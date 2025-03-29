import jsonfile from"jsonfile";
import moment from "moment";

const path = "./data.json";
const date = moment().format();

const data = {
    date: date,
};
jsonfile.writefile(path, data);     