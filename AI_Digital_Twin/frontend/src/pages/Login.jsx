import {useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";

function Login(){

const[email,setEmail]=useState("");
const[password,setPassword]=useState("");

const navigate=useNavigate();

async function login(){

try{

const response=await axios.post(
"http://127.0.0.1:8000/login",
{
email,
password
}
);

localStorage.setItem(
"token",
response.data.token
);

navigate("/chat");

}
catch(error){

alert("Login failed");

}

}

return(

<div className="container">

<div className="card">

<h2>Login</h2>

<input
placeholder="Email"
onChange={(e)=>setEmail(e.target.value)}
/>

<input
type="password"
placeholder="Password"
onChange={(e)=>setPassword(e.target.value)}
/>

<button onClick={login}>
Login
</button>

</div>

</div>

)

}

export default Login;