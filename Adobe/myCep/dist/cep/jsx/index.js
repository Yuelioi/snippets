(function (thisObj) {

var config = {
  version: version,
  id: "com.bolt.cep",
  displayName: "Bolt CEP",
  symlink: "local",
  port: 3000,
  servePort: 5000,
  startingDebugPort: 8860,
  extensionManifestVersion: 6.0,
  requiredRuntimeVersion: 9.0,
  hosts: [{
    name: "AEFT",
    version: "[0.0,99.9]"
  }, {
    name: "PPRO",
    version: "[0.0,99.9]"
  }, {
    name: "ILST",
    version: "[0.0,99.9]"
  }, {
    name: "PHXS",
    version: "[0.0,99.9]"
  }, {
    name: "FLPR",
    version: "[0.0,99.9]"
  }],
  type: "Panel",
  iconDarkNormal: "./src/assets/light-icon.png",
  iconNormal: "./src/assets/dark-icon.png",
  iconDarkNormalRollOver: "./src/assets/light-icon.png",
  iconNormalRollOver: "./src/assets/dark-icon.png",
  parameters: ["--v=0", "--enable-nodejs", "--mixed-context"],
  width: 500,
  height: 550,
  panels: [{
    mainPath: "./main/index.html",
    name: "main",
    panelDisplayName: "Bolt CEP",
    autoVisible: true,
    width: 600,
    height: 650
  }],
  build: {
    jsxBin: "off",
    sourceMap: true
  },
  zxp: {
    country: "US",
    province: "CA",
    org: "MyCompany",
    password: "mypassword",
    tsa: "http://timestamp.digicert.com/",
    sourceMap: false,
    jsxBin: "off"
  },
  installModules: [],
  copyAssets: [],
  copyZipAssets: []
};

var ns = config.id;

var helloError = function helloError(str) {
  // Intentional Error for Error Handling Demonstration
  
  strr;
};
var helloStr = function helloStr(str) {
  alert("ExtendScript received a string: ".concat(str));
  return str;
};
var helloNum = function helloNum(n) {
  alert("ExtendScript received a number: ".concat(n.toString()));
  return n;
};
var helloArrayStr = function helloArrayStr(arr) {
  alert("ExtendScript received an array of ".concat(arr.length, " strings: ").concat(arr.toString()));
  return arr;
};
var helloObj = function helloObj(obj) {
  alert("ExtendScript received an object: ".concat(JSON.stringify(obj)));
  return {
    y: obj.height,
    x: obj.width
  };
};

var helloWorld$4 = function helloWorld() {
  alert("Hello from After Effe2");
  var activeComp = app.project.activeItem;
  alert(activeComp ? activeComp.name : '没有活动项目');
};

var aeft = /*#__PURE__*/__objectFreeze({
  __proto__: null,
  helloError: helloError,
  helloStr: helloStr,
  helloNum: helloNum,
  helloArrayStr: helloArrayStr,
  helloObj: helloObj,
  helloWorld: helloWorld$4
});

var helloWorld$3 = function helloWorld() {
  alert("Hello from Illustrator");
  app.activeDocument.path;
};

var ilst = /*#__PURE__*/__objectFreeze({
  __proto__: null,
  helloError: helloError,
  helloStr: helloStr,
  helloNum: helloNum,
  helloArrayStr: helloArrayStr,
  helloObj: helloObj,
  helloWorld: helloWorld$3
});

var helloWorld$2 = function helloWorld() {
  alert("Hello from Animate");
};

var anim = /*#__PURE__*/__objectFreeze({
  __proto__: null,
  helloWorld: helloWorld$2
});

var qeDomFunction = function qeDomFunction() {
  if (typeof qe === "undefined") {
    app.enableQE();
  }
  if (qe) {
    qe.name;
    qe.project.getVideoEffectByName("test");
  }
};
var helloWorld$1 = function helloWorld() {
  alert("Hello from Premiere Pro.");
};

var ppro = /*#__PURE__*/__objectFreeze({
  __proto__: null,
  helloError: helloError,
  helloStr: helloStr,
  helloNum: helloNum,
  helloArrayStr: helloArrayStr,
  helloObj: helloObj,
  qeDomFunction: qeDomFunction,
  helloWorld: helloWorld$1
});

var helloWorld = function helloWorld() {
  app.activeDocument;
  alert("Hello from Photoshop");
};

var phxs = /*#__PURE__*/__objectFreeze({
  __proto__: null,
  helloError: helloError,
  helloStr: helloStr,
  helloNum: helloNum,
  helloArrayStr: helloArrayStr,
  helloObj: helloObj,
  helloWorld: helloWorld
});

var main;
switch (BridgeTalk.appName) {
  case "premierepro":
  case "premiereprobeta":
    main = ppro;
    break;
  case "aftereffects":
  case "aftereffectsbeta":
    main = aeft;
    break;
  case "illustrator":
  case "illustratorbeta":
    main = ilst;
    break;
  case "photoshop":
  case "photoshopbeta":
    main = phxs;
    break;
  default:
    
    if (app.appName === "Adobe Animate") {
      main = anim;
    }
    break;
}

var host = typeof $ !== "undefined" ? $ : window;
host[ns] = main;
