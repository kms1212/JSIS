import { instance } from "@/scripts/api/axios.js";

export async function getMeal(options = {}) {
  if (options.mdate && options.mtime) {
    const response = await instance.get("/meal/", {
      params: {
        mdate: options.mdate,
        mtime: options.mtime,
      },
    });

    if (response.status == 200) {
      return response.data;
    }
  } else {
    const response = await instance.get("/meal/");
    if (response.status == 200) {
      return response.data;
    }
  }
}
