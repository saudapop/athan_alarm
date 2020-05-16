import React from "react";
import ReactDOM from "react-dom";
import { App } from "./app";
import axios from "axios";

console.log("assalamualaikum wa rahmutullahi wa barakatuhu");

// axios.get("/api/get-preferences/").then((res) => console.log(res));

// axios
//   .post("/api/update-scheduler/", {
//     Dhuhr: 1,
//     Asr: 1,
//     Maghrib: 1,
//     Fajr: 1,
//     Isha: 1,
//   })
//   .then((res) => console.log(res))
//   .catch((e) => console.log(e));

ReactDOM.render(<App />, document.getElementById("root"));
