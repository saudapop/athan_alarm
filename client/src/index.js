import axios from "axios";

console.log("assalamualaikum wa rahmutullahi wa barakatuhu");

axios.get("/api/get-preferences/").then((res) => console.log(res));
