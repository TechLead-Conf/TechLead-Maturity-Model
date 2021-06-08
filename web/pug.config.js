const path = require("path");
const fs = require("fs");
const toml = require("toml");

const dataPath = path.join(__dirname, "..", "src");

function readDir(dirPath) {
  const data = {};

  const dir = fs.opendirSync(dirPath);

  let dirent;
  while ((dirent = dir.readSync()) !== null) {
    const fileData = fs.readFileSync(path.join(dirPath, dirent.name), {
      encoding: "utf8",
      flag: "r",
    });
    data[dirent.name.replace(".toml", "")] = toml.parse(fileData);
  }

  dir.closeSync();

  return data;
}

const matrix_data = {
  categories: readDir(path.join(dataPath, "categories")),
  levels: readDir(path.join(dataPath, "levels")),
  skills: readDir(path.join(dataPath, "skills")),
};

module.exports = {
  locals: matrix_data,
};
