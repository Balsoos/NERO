import React from "react";
import ChatBox from "../components/Chat/ChatBox";

function ChatPage({ token }) {
    return (
        <div>
            <h1>Chat with NERO</h1>
            <ChatBox token={token} />
        </div>
    );
}

export default ChatPage;
