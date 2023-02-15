import { instance } from "@/scripts/api/axios.js";
import { getFileInfo } from "@/scripts/api/file.js";

export async function getCommunityArticle(id) {
  const response = await instance.get(`/community/article/`, {
    params: {
      articleid: id,
    },
  });

  response.data.files_fileinfo = await getCommunityArticleFileInfo(
    response.data.files
  );

  return response.data;
}

export async function getCommunityArticleList(params) {
  const response = await instance.get(`/community/article/`, {
    params: params,
  });

  return response.data;
}

export async function likeCommunityArticle(id) {
  const response = await instance.post(`/community/article/like/`, {
    articleid: id,
  });

  return response.data;
}

async function getCommunityArticleFileInfo(fileidlist) {
  const fileinfolist = [];

  for (var fileid of fileidlist) {
    const file = await getFileInfo(fileid);
    fileinfolist.push(file);
  }

  return fileinfolist;
}

export default {
  getCommunityArticle,
  getCommunityArticleList,
};
