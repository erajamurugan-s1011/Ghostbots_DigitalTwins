import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Chat() {

    const navigate = useNavigate();

    const [message, setMessage] = useState("");
    const [file, setFile] = useState(null);
    const [chats, setChats] = useState([]);

    useEffect(() => {

        loadHistory();

    }, []);


    async function loadHistory() {

        try {

            const response = await axios.get(
                "http://127.0.0.1:8000/history",
                {
                    headers: {
                        Authorization:
                            `Bearer ${localStorage.getItem("token")}`
                    }
                }
            );

            setChats(response.data);

        }
        catch(error){

            console.log(error);

        }

    }


    async function uploadFile() {

        if (!file) {

            alert("Choose a file");
            return;

        }

        const formData = new FormData();

        formData.append(
            "file",
            file
        );

        try {

            await axios.post(
                "http://127.0.0.1:8000/upload",
                formData,
                {
                    headers: {
                        Authorization:
                            `Bearer ${localStorage.getItem("token")}`
                    }
                }
            );

            alert(
                "Digital Twin uploaded successfully"
            );

        }
        catch(error){

            console.log(error);

        }

    }


    async function sendMessage() {

        if (!message) return;

        try {

            const response = await axios.post(
                "http://127.0.0.1:8000/chat",
                {
                    message
                },
                {
                    headers: {
                        Authorization:
                            `Bearer ${localStorage.getItem("token")}`
                    }
                }
            );

            const newChat = {

                question: message,
                answer: response.data.reply

            };

            setChats(
                [...chats, newChat]
            );

            setMessage("");

        }
        catch(error){

            console.log(error);

            if(
                error.response?.status===401
            ){

                localStorage.removeItem(
                    "token"
                );

                navigate("/");

            }

        }

    }

    return (

        <div className="container">

            <h1>
                👻 AI Ghostbot
            </h1>


            <div className="card">

                <h3>
                    Upload Digital Twin Data
                </h3>

                <input
                    type="file"
                    onChange={(e)=>
                        setFile(
                            e.target.files[0]
                        )
                    }
                />

                <button
                    onClick={uploadFile}
                >
                    Upload
                </button>

            </div>


            <div className="card">

                <h3>
                    Chat
                </h3>

                <div
                    className="chat-box"
                >

                    {chats.map(
                        (
                            chat,
                            index
                        )=>(
                        <div
                        key={index}
                        >

                        <div
                        className="user-message"
                        >
                        {chat.question}
                        </div>

                        <div
                        className="bot-message"
                        >
                        {chat.answer}
                        </div>

                        </div>
                    ))}

                </div>

                <input
                    value={message}
                    onChange={(e)=>
                        setMessage(
                            e.target.value
                        )
                    }
                    placeholder="Ask something..."
                />

                <button
                    onClick={sendMessage}
                >
                    Send
                </button>

            </div>

        </div>

    );

}

export default Chat;