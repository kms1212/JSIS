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

export default {
  getFileInfo,
  getFile,
};
