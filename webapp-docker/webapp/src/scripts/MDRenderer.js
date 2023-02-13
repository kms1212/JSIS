import { marked } from "marked";
import hljs from "highlightjs";

const renderer = new marked.Renderer();

renderer.heading = function (text, level) {
  let text_size;
  let font_weight;
  let additional = "";

  switch (level) {
    case 1:
      text_size = "text-3xl";
      font_weight = "font-bold";
      additional = '<hr class="mb-6"/>';
      break;
    case 2:
      text_size = "text-2xl";
      font_weight = "font-bold";
      additional = '<hr class="mb-6"/>';
      break;
    case 3:
      text_size = "text-xl";
      font_weight = "font-bold";
      break;
    case 4:
      text_size = "text-lg";
      font_weight = "font-bold";
      break;
    case 5:
      text_size = "text-lg";
      font_weight = "font-semibold";
      break;
    case 6:
      text_size = "text-lg";
      font_weight = "font-medium";
      break;
    default:
      text_size = "text-base";
      font_weight = "font-bold";
  }

  return (
    "<h" +
    level +
    ' class="mb-2 mt-5 ' +
    text_size +
    " " +
    font_weight +
    '">' +
    text +
    "</h" +
    level +
    ">" +
    additional
  );
};

renderer.paragraph = function (text) {
  return '<p class="mb-2">' + text + "</p>";
};

renderer.list = function (body, ordered) {
  var type = ordered ? "ol" : "ul";
  return (
    "<" + type + ' class="list-disc ml-4 mb-2">' + body + "</" + type + ">"
  );
};

renderer.listitem = function (text) {
  return '<li class="mb-1">' + text + "</li>";
};

renderer.table = function (header, body) {
  if (body) {
    body = "<tbody>" + body + "</tbody>";
  }
  return (
    '<table class="border-collapse border border-black">' +
    "<thead>" +
    header +
    "</thead>" +
    body +
    "</table>"
  );
};

renderer.tablerow = function (content) {
  return "<tr>" + content + "</tr>";
};

renderer.tablecell = function (content, flags) {
  var type = flags.header ? "th" : "td";
  var tag = flags.align
    ? "<" +
      type +
      ' style="text-align:' +
      flags.align +
      '" class="border border-black py-1 px-2 ' +
      (flags.header ? "bg-gray-100 font-semibold" : "") +
      '">'
    : "<" +
      type +
      ' class="border border-black py-1 px-2 ' +
      (flags.header ? "bg-gray-100 font-semibold" : "") +
      '">';
  return tag + content + "</" + type + ">";
};

renderer.strong = function (text) {
  return '<strong class="font-semibold">' + text + "</strong>";
};

renderer.em = function (text) {
  return '<em class="italic">' + text + "</em>";
};

renderer.code = function (code) {
  return (
    '<pre class="bg-gray-200 rounded-lg p-4 mt-2 mb-5 overflow-scroll"><code>' +
    hljs.highlightAuto(code).value +
    "</code></pre>"
  );
};

renderer.codespan = function (text) {
  return '<code class="bg-gray-200 px-1 rounded">' + text + "</code>";
};

renderer.blockquote = function (quote) {
  return (
    '<blockquote class="border-l-4 border-gray-400 italic pl-2 mb-2">' +
    quote +
    "</blockquote>"
  );
};

renderer.html = function (html) {
  return html;
};

renderer.hr = function () {
  return '<hr class="border-gray-400 border-2 mt-2 mb-5">';
};

renderer.br = function () {
  return "<br>";
};

renderer.del = function (text) {
  return "<del>" + text + "</del>";
};

renderer.link = function (href, title, text) {
  return (
    '<a href="' +
    href +
    '" title="' +
    title +
    '" class="text-blue-500">' +
    text +
    "</a>"
  );
};

renderer.image = function (href, title, text) {
  return (
    '<img src="' +
    href +
    '" alt="' +
    text +
    '" title="' +
    title +
    '" class="mb-2">'
  );
};

renderer.text = function (text) {
  return text;
};

marked.setOptions({
  renderer: renderer,
  gfm: true,
  tables: true,
  breaks: true,
  pedantic: false,
  sanitize: false,
  smartLists: true,
  smartypants: true,
});

export default marked;
