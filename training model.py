import tensorflow as tf
import keras_cv
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# --- DIAGNOSTIC LINES START ---
print(f"Keras-CV Version: {keras_cv.__version__}")

# Check what's available directly under keras_cv.models
print("\nContents of keras_cv.models (first 20 attributes):")
model_attributes = [name for name in dir(keras_cv.models) if not name.startswith('_')]
print(model_attributes[:20]) # Print only the first few to keep output concise

# Check specifically if 'ConvNeXtV2Backbone' exists in keras_cv.models
if hasattr(keras_cv.models, 'ConvNeXtV2Backbone'):
    print("\n'ConvNeXtV2Backbone' IS found in keras_cv.models!")
else:
    print("\n'ConvNeXtV2Backbone' is NOT found in keras_cv.models.")

# Check if keras_cv.api.models exists and what it contains (relevant to your error)
if hasattr(keras_cv.api, 'models'):
    print("\n'keras_cv.api.models' EXISTS.")
    api_models_attributes = [name for name in dir(keras_cv.api.models) if not name.startswith('_')]
    print("Contents of keras_cv.api.models (first 20 attributes):")
    print(api_models_attributes[:20])
    if hasattr(keras_cv.api.models, 'ConvNeXtV2Backbone'):
        print("\n'ConvNeXtV2Backbone' IS found in keras_cv.api.models!")
    else:
        print("\n'ConvNeXtV2Backbone' is NOT found in keras_cv.api.models.")
else:
    print("\n'keras_cv.api.models' DOES NOT EXIST.")
# --- DIAGNOSTIC LINES END ---

# Check what presets are available for ResNetV2Backbone
print("\nAvailable presets for ResNetV2Backbone:")
try:
    print(keras_cv.models.ResNetV2Backbone.presets.keys())
except Exception as e:
    print(f"Error checking presets: {e}")

# --- 0. Set up Mixed Precision (Highly Recommended for Modern GPUs) ---
# Commented out mixed precision for better compatibility
# tf.keras.mixed_precision.set_global_policy('mixed_float16')


# --- 1. Load and Prepare Data ---

IMG_HEIGHT = 32  # Use native CIFAR-10 size for speed
IMG_WIDTH = 32   # Use native CIFAR-10 size for speed
NUM_CLASSES = 10
BATCH_SIZE = 32
EPOCHS_PHASE1 = 2   # Fewer epochs for quick runs
EPOCHS_PHASE2 = 2   # Fewer epochs for quick runs

# Speed-up toggles
USE_SIMPLE_MODEL = True  # Force a small CNN for fast execution
TRAIN_SAMPLES = 10000    # Subset training set for speed (max 50000)
TEST_SAMPLES = 2000      # Subset test set for speed (max 10000)

(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Use only a subset to speed up iterations
x_train, y_train = x_train[:TRAIN_SAMPLES], y_train[:TRAIN_SAMPLES]
x_test, y_test = x_test[:TEST_SAMPLES], y_test[:TEST_SAMPLES]

x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

y_train = tf.keras.utils.to_categorical(y_train, NUM_CLASSES)
y_test = tf.keras.utils.to_categorical(y_test, NUM_CLASSES)

print(f"x_train shape: {x_train.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"x_test shape: {x_test.shape}")
print(f"y_test shape: {y_test.shape}")

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
    ],
    name="data_augmentation",
)

train_ds = (
    tf.data.Dataset.from_tensor_slices((x_train, y_train))
    .shuffle(10000)
    .batch(BATCH_SIZE)
    .map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=tf.data.AUTOTUNE)
    .prefetch(tf.data.AUTOTUNE)
)

test_ds = (
    tf.data.Dataset.from_tensor_slices((x_test, y_test))
    .batch(BATCH_SIZE)
    .cache()
    .prefetch(tf.data.AUTOTUNE)
)


# --- 2. Define Model: Load ResNetV2 and adapt for CIFAR-10 ---

if USE_SIMPLE_MODEL:
    print("Using simple CNN for fast execution...")
    base_model = keras.Sequential([
        layers.Conv2D(32, 3, activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 3, activation='relu'),
        layers.GlobalAveragePooling2D()
    ])
else:
    # Try to use ResNetV2Backbone with available presets, fallback to simple model if needed
    try:
        # Check available presets first
        available_presets = list(keras_cv.models.ResNetV2Backbone.presets.keys())
        print(f"Available presets: {available_presets}")
        
        if available_presets:
            # Use the first available preset
            preset_name = available_presets[0]
            print(f"Using preset: {preset_name}")
            base_model = keras_cv.models.ResNetV2Backbone.from_preset(
                preset_name,
                input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
                include_rescaling=False
            )
        else:
            # Fallback to simple ResNetV2 without preset
            base_model = keras_cv.models.ResNetV2Backbone(
                input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
                include_rescaling=False
            )
    except Exception as e:
        print(f"Error with ResNetV2Backbone: {e}")
        print("Falling back to simple CNN model...")
        # Fallback to a simple CNN if keras_cv models fail
        base_model = keras.Sequential([
            layers.Conv2D(32, 3, activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, activation='relu'),
            layers.GlobalAveragePooling2D()
        ])

# Build the model based on what base_model we got
if isinstance(base_model, keras.Sequential):
    # If we're using the fallback CNN, add the classification head directly to Sequential
    base_model.add(layers.Dense(128, activation='relu'))
    base_model.add(layers.Dense(NUM_CLASSES, activation="softmax", dtype="float32"))
    model = base_model
else:
    # If we're using keras_cv backbone, build the full model
    inputs = keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3))
    x = base_model(inputs)
    x = layers.GlobalAveragePooling2D()(x)
    outputs = layers.Dense(NUM_CLASSES, activation="softmax", dtype="float32")(x)
    model = keras.Model(inputs, outputs)

model.summary()


# --- 3. Training Phase 1: Train only the classification head (with frozen backbone) ---

base_model.trainable = False

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("\nStarting Phase 1 Training (Frozen Backbone, Training Head)...")
history_phase1 = model.fit(
    train_ds,
    epochs=EPOCHS_PHASE1,
    validation_data=test_ds,
    callbacks=[
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
    ]
)
print("Phase 1 finished.")


# --- 4. Training Phase 2: Fine-tune the entire model (unfreeze backbone) ---

base_model.trainable = True

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("\nStarting Phase 2 Training (Unfrozen Backbone - Fine-tuning)...")
history_phase2 = model.fit(
    train_ds,
    epochs=EPOCHS_PHASE2,
    validation_data=test_ds,
    callbacks=[
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-7),
        ModelCheckpoint('best_resnet_v2_cifar10_model.keras', monitor='val_accuracy', save_best_only=True, mode='max')
    ]
)
print("Phase 2 finished.")


# --- 5. Evaluate Model ---
print("\nEvaluating final model...")
loss, accuracy = model.evaluate(test_ds)
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {accuracy:.4f}")

# --- Optional: Plot training history ---
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history_phase1.history['accuracy'] + history_phase2.history['accuracy'], label='Training Accuracy')
plt.plot(history_phase1.history['val_accuracy'] + history_phase2.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history_phase1.history['loss'] + history_phase2.history['loss'], label='Training Loss')
plt.plot(history_phase1.history['val_loss'] + history_phase2.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig("training_curves.png")
plt.close()

# --- Optional: Make predictions on a few test images ---
class_names = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

plt.figure(figsize=(10, 10))
for images, labels in test_ds.take(1):
    predictions = model.predict(images)
    for i in range(min(16, images.shape[0])):
        ax = plt.subplot(4, 4, i + 1)
        plt.imshow(images[i])
        predicted_label = np.argmax(predictions[i])
        true_label = np.argmax(labels[i])
        color = 'green' if predicted_label == true_label else 'red'
        plt.title(f"Pred: {class_names[predicted_label]}\nTrue: {class_names[true_label]}", color=color)
        plt.axis("off")
plt.suptitle("Predictions on Test Images", fontsize=16)
plt.tight_layout()
plt.savefig("predictions.png")
plt.close()

# --- Additional Visualizations ---

# 1. Confusion Matrix
print("\nGenerating confusion matrix...")
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

# Get predictions for all test data
all_predictions = []
all_true_labels = []

for images, labels in test_ds:
    predictions = model.predict(images, verbose=0)
    all_predictions.extend(np.argmax(predictions, axis=1))
    all_true_labels.extend(np.argmax(labels.numpy(), axis=1))

# Create confusion matrix
cm = confusion_matrix(all_true_labels, all_predictions)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()

# 2. Classification Report
print("Generating classification report...")
report = classification_report(all_true_labels, all_predictions, 
                              target_names=class_names, output_dict=True)

# Convert to DataFrame for better visualization
import pandas as pd
report_df = pd.DataFrame(report).transpose()
report_df = report_df.drop('support', axis=1)  # Remove support column for cleaner plot

plt.figure(figsize=(12, 8))
sns.heatmap(report_df, annot=True, cmap='YlOrRd', fmt='.3f')
plt.title('Classification Report Heatmap')
plt.tight_layout()
plt.savefig("classification_report.png")
plt.close()

# 3. Per-Class Accuracy Bar Chart
print("Generating per-class accuracy chart...")
class_accuracy = []
for i in range(NUM_CLASSES):
    mask = np.array(all_true_labels) == i
    if np.sum(mask) > 0:
        accuracy = np.sum(np.array(all_predictions)[mask] == i) / np.sum(mask)
        class_accuracy.append(accuracy)
    else:
        class_accuracy.append(0)

plt.figure(figsize=(12, 6))
bars = plt.bar(class_names, class_accuracy, color='skyblue', edgecolor='navy')
plt.title('Per-Class Accuracy')
plt.xlabel('Classes')
plt.ylabel('Accuracy')
plt.xticks(rotation=45)
plt.ylim(0, 1)

# Add value labels on bars
for bar, acc in zip(bars, class_accuracy):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
             f'{acc:.3f}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig("per_class_accuracy.png")
plt.close()

# 4. Learning Rate Schedule Visualization
print("Generating learning rate visualization...")
epochs = list(range(1, len(history_phase1.history['accuracy']) + len(history_phase2.history['accuracy']) + 1))
lr_phase1 = [1e-3] * len(history_phase1.history['accuracy'])
lr_phase2 = [1e-5] * len(history_phase2.history['accuracy'])
learning_rates = lr_phase1 + lr_phase2

plt.figure(figsize=(10, 6))
plt.plot(epochs, learning_rates, 'b-', linewidth=2, marker='o')
plt.title('Learning Rate Schedule')
plt.xlabel('Epoch')
plt.ylabel('Learning Rate')
plt.yscale('log')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("learning_rate_schedule.png")
plt.close()

# 5. Model Predictions Confidence Distribution
print("Generating confidence distribution...")
all_confidences = []
for images, labels in test_ds:
    predictions = model.predict(images, verbose=0)
    max_confidences = np.max(predictions, axis=1)
    all_confidences.extend(max_confidences)

plt.figure(figsize=(10, 6))
plt.hist(all_confidences, bins=50, alpha=0.7, color='green', edgecolor='black')
plt.title('Distribution of Prediction Confidence')
plt.xlabel('Confidence Score')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("confidence_distribution.png")
plt.close()

# 6. Training vs Validation Metrics Comparison
print("Generating detailed metrics comparison...")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Accuracy comparison
axes[0, 0].plot(history_phase1.history['accuracy'] + history_phase2.history['accuracy'], 
                label='Training Accuracy', marker='o')
axes[0, 0].plot(history_phase1.history['val_accuracy'] + history_phase2.history['val_accuracy'], 
                label='Validation Accuracy', marker='s')
axes[0, 0].set_title('Accuracy Over Time')
axes[0, 0].set_xlabel('Epoch')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Loss comparison
axes[0, 1].plot(history_phase1.history['loss'] + history_phase2.history['loss'], 
                label='Training Loss', marker='o')
axes[0, 1].plot(history_phase1.history['val_loss'] + history_phase2.history['val_loss'], 
                label='Validation Loss', marker='s')
axes[0, 1].set_title('Loss Over Time')
axes[0, 1].set_xlabel('Epoch')
axes[0, 1].set_ylabel('Loss')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Phase separation
phase1_epochs = list(range(1, len(history_phase1.history['accuracy']) + 1))
phase2_epochs = list(range(len(history_phase1.history['accuracy']) + 1, 
                          len(history_phase1.history['accuracy']) + len(history_phase2.history['accuracy']) + 1))

axes[1, 0].plot(phase1_epochs, history_phase1.history['accuracy'], 'b-', label='Phase 1 Training', marker='o')
axes[1, 0].plot(phase1_epochs, history_phase1.history['val_accuracy'], 'b--', label='Phase 1 Validation', marker='s')
axes[1, 0].plot(phase2_epochs, history_phase2.history['accuracy'], 'r-', label='Phase 2 Training', marker='o')
axes[1, 0].plot(phase2_epochs, history_phase2.history['val_accuracy'], 'r--', label='Phase 2 Validation', marker='s')
axes[1, 0].set_title('Training Phases Comparison')
axes[1, 0].set_xlabel('Epoch')
axes[1, 0].set_ylabel('Accuracy')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Error rate
train_error = [1 - acc for acc in history_phase1.history['accuracy'] + history_phase2.history['accuracy']]
val_error = [1 - acc for acc in history_phase1.history['val_accuracy'] + history_phase2.history['val_accuracy']]

axes[1, 1].plot(epochs, train_error, label='Training Error Rate', marker='o')
axes[1, 1].plot(epochs, val_error, label='Validation Error Rate', marker='s')
axes[1, 1].set_title('Error Rate Over Time')
axes[1, 1].set_xlabel('Epoch')
axes[1, 1].set_ylabel('Error Rate')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("detailed_metrics_comparison.png")
plt.close()

print("\nAll visualizations completed!")
print("Generated files:")
print("- confusion_matrix.png")
print("- classification_report.png") 
print("- per_class_accuracy.png")
print("- learning_rate_schedule.png")
print("- confidence_distribution.png")
print("- detailed_metrics_comparison.png")

# Print the current working directory
import os
print(f"\nFiles saved in: {os.getcwd()}")
print("You can find all PNG files in the above directory.")