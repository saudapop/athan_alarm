import axios from "axios";

console.log("assalamualaikum wa rahmutullahi wa barakatuhu");

axios
  .get("http://0.0.0.0:25526/api/get-preferences/")
  .then((res) => console.log(res));
