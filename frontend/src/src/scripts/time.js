import moment from "moment";

export function getSimplifiedTimestamp(timestamp) {
  const mtimestamp = moment(timestamp);
  const now = moment();
  const yesterday = moment().subtract(1, "day");
  const theDayBeforeYesterday = moment().subtract(2, "day");

  console.log(now);
  console.log(mtimestamp);

  if (mtimestamp.isSame(now, "minute")) {
    const passedSeconds = Math.floor(
      moment.duration(mtimestamp.diff(now)).asSeconds()
    );
    return Math.abs(passedSeconds) + "초 전";
  } else if (mtimestamp.isSame(now, "hour")) {
    const passedMinutes = Math.floor(
      moment.duration(mtimestamp.diff(now)).asMinutes()
    );
    return Math.abs(passedMinutes) + "분 전";
  } else if (mtimestamp.isSame(now, "day")) {
    const passedTime = Math.floor(
      moment.duration(mtimestamp.diff(now)).asHours()
    );
    return Math.abs(passedTime) + "시간 전";
  } else if (mtimestamp.isSame(yesterday, "day")) {
    return "어제";
  } else if (mtimestamp.isSame(theDayBeforeYesterday, "day")) {
    return "그저께";
  } else if (mtimestamp.isSame(now, "month")) {
    const passedDays = Math.floor(
      moment.duration(mtimestamp.diff(now)).asDays()
    );
    return Math.abs(passedDays) + "일 전";
  } else {
    return mtimestamp.format("YYYY-MM-DD");
  }
}
