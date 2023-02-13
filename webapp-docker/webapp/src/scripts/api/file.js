import { instance } from "@/scripts/api/axios.js";

export async function getFileInfo(id) {
  const response = await instance.get(`/api/file/info/`, {
    params: {
      fileid: id,
    },
  });

  return response.data;
}

export async function getFile(id) {
  const response = await instance.get(`/api/file/`, {
    params: {
      fileid: id,
    },
    responseType: "blob",
  });

  return response.data;
}

export async function readFileAsDataURL(file) {
  let result_base64 = await new Promise((resolve) => {
    let fileReader = new FileReader();
    fileReader.onload = () => resolve(fileReader.result);
    fileReader.readAsDataURL(file);
  });

  return result_base64;
}

export default {
  getFileInfo,
  getFile,
};
