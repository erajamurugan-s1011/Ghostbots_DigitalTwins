import {useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";

function Register(){

const[username,setUsername]=useState("");
const[email,setEmail]=useState("");
const[password,setPassword]=useState("");

const navigate=useNavigate();

async function register(){

try{

await axios.post(
"http://127.0.0.1:8000/register",
{
username,
email,
password
}
);

alert(
"Registration successful"
);

navigate("/");

}
catch(error){

alert(
"Registration failed"
);

}

}

return(

<div className="container">

<div className="card">

<h2>Register</h2>

<input
placeholder="Username"
onChange={(e)=>setUsername(e.target.value)}
/>

<input
placeholder="Email"
onChange={(e)=>setEmail(e.target.value)}
/>

<input
type="password"
placeholder="Password"
onChange={(e)=>setPassword(e.target.value)}
/>

<button onClick={register}>
Register
</button>

</div>

</div>

)

}

export default Register;