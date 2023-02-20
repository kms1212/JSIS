import { instance } from "@/scripts/api/axios.js";

export async function getReplyList(options = {}) {
  if (options.articleid) {
    const response = await instance.get("/mainbbs/reply/", {
      params: {
        articleid: options.articleid,
      },
    });

    if (response.status === 200) {
      return response.data;
    }
  } else if (options.replyid) {
    const response = await instance.get("/mainbbs/reply/", {
      params: {
        replyid: options.replyid,
      },
    });

    if (response.status === 200) {
      return response.data;
    }
  } else {
    return;
  }
}
