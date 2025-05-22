import HeroCarousel from "../components/HeroCarousel";
import RecentArticles from "../components/RecentArticles";
import Sidebar from "../components/Sidebar";

export default function HomePage() {
return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white">
      {/* Hero Section with drop shadow */}
    <div className="container mx-auto px-4 py-8">
        <HeroCarousel />
    </div>

      {/* Main Content */}
    <div className="container mx-auto px-4 flex flex-col md:flex-row gap-8 mt-4 animate-fade-in">
        {/* Articles */}
        <div className="flex-1 bg-gray-800 p-6 rounded-xl shadow-lg">
        <h2 className="text-2xl font-bold mb-4 border-b border-gray-600 pb-2">Latest Articles</h2>
        <RecentArticles />
        </div>

        {/* Sidebar */}
        <div className="w-full md:w-1/3 bg-gray-800 p-6 rounded-xl shadow-lg">
        <Sidebar />
        </div>
    </div>
    </div>
);
}
