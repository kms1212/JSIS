import moment from "moment";

export function getSimplifiedTimestamp(timestamp) {
  const mtimestamp = moment(timestamp);
  const now = moment();
  const yesterday = moment().subtract(1, "day");
  const theDayBeforeYesterday = moment().subtract(2, "day");

  console.log(now);
  console.log(mtimestamp);

  if (mtimestamp.isSame(now, "day")) {
    const passedTime = moment.duration(mtimestamp.diff(now)).asHours();
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
