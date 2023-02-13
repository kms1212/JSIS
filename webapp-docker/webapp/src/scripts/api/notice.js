import { instance } from "@/scripts/api/axios.js";
import { getFileInfo } from "@/scripts/api/file.js";

export async function getNoticeArticle(id) {
  const response = await instance.get(`/api/mainbbs/article/`, {
    params: {
      articleid: id,
    },
  });

  response.data.files_fileinfo = await getNoticeArticleFileInfo(
    response.data.files
  );

  return response.data;
}

export async function getNoticeArticleList(params) {
  const response = await instance.get(`/api/mainbbs/article/`, {
    params: params,
  });

  return response.data;
}

export async function likeNoticeArticle(id) {
  const response = await instance.post(
    `/api/mainbbs/like/`,
    {},
    {
      params: {
        articleid: id,
      },
    }
  );

  return response.data;
}

async function getNoticeArticleFileInfo(fileidlist) {
  const fileinfolist = [];

  for (var fileid of fileidlist) {
    const file = await getFileInfo(fileid);
    fileinfolist.push(file);
  }

  return fileinfolist;
}

export default {
  getNoticeArticle,
  getNoticeArticleList,
};
