import axios from "axios";

console.log("assalamualaikum wa rahmutullahi wa barakatuhu");

axios.get("/api/get-preferences/").then((res) => console.log(res));

axios
  .post("/api/update-scheduler/", {
    Dhuhr: 0,
    Asr: 0,
    Maghrib: 1,
  })
  .then((res) => console.log(res))
  .catch((e) => console.log(e));
