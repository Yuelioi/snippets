import {
    helloError,
    helloStr,
    helloNum,
    helloArrayStr,
    helloObj,
} from "../utils/samples";
export { helloError, helloStr, helloNum, helloArrayStr, helloObj };

export const helloWorld = () => {
    alert("Hello from After Effects!");
    app.project.activeItem;
};
export const openProjFolder = (num: number) => {
    alert("EAA");
    Folder(File((app as any).project.file).parent.fsName).execute();
};