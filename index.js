import jsonfile from"jsonfile";
import moment from "moment";
import random from "random";


const path = "./data.json";
const makecommits = (n)=>{
    if(n===0) return simpleGit().push();
    const x = random.default.int(0, 54);
    const y = random.default.int(0, 6);
    const date = moment().subtract(1, "y").add(1, "d").add(x, "w").add(y, "d").format();
}

const data = {
    date: date,
};
console.log(date);
jsonfile.writefile(path, data,()=> {
    simpleGit().add([path]).commit(date, {"--date": date}, makecommits.bind(this,--n));
});
makecommits(100);