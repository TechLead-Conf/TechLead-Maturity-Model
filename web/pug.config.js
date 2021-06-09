const path = require("path");
const fs = require("fs");
const toml = require("toml");

const dataPath = path.join(__dirname, "..", "src");

function readTomlFile(filePath) {
  const fileData = fs.readFileSync(filePath, {
    encoding: "utf8",
    flag: "r",
  });
  return toml.parse(fileData);
}

function readTomlDir(dirPath) {
  const data = {};

  const dir = fs.opendirSync(dirPath);

  let dirent;
  while ((dirent = dir.readSync()) !== null) {
    data[dirent.name.replace(".toml", "")] = readTomlFile(
      path.join(dirPath, dirent.name)
    );
  }

  dir.closeSync();

  return data;
}

const matrix_data = {
  categories: readTomlDir(path.join(dataPath, "categories")),
  levels: readTomlDir(path.join(dataPath, "levels")),
  skills: readTomlDir(path.join(dataPath, "skills")),
  matrix: readTomlFile(path.join(dataPath, "matrix.toml")),
};

module.exports = {
  locals: matrix_data,
};
