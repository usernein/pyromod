import styles from './styles.module.css';
import {useEffect, useRef, useState} from "react";

const controller = {
    setMessages: () => {
    },
    updateCallback: () => {
    }
}

const sendMessage = (message) => {
    if (message) {
        const msgObj = {
            "type": "text",
            "value": message,
            "outgoing": true
        }
        controller.setMessages((messages) => [msgObj, ...messages]);

        const response = controller.updateCallback(msgObj);
        if (response) {
            const responseObj = {
                "type": "text",
                "value": response,
                "outgoing": false
            }
            setTimeout(() => {
                controller.setMessages((messages) => [responseObj, ...messages]);
            }, 300);
        }
    }
}

const Command = ({command}) => {
    return (
        <div className={"text-blue-500 inline cursor-pointer"} onClick={() => sendMessage(command)}>
            {command}
        </div>
    )
}


const ChatMessage = ({message, outgoing}) => {
    let innerBubble = [message];

    // replace all texts that start with slash for Command instance instead
    const commandRegex = /\/[a-zA-Z0-9]+/g;
    const commands = message.match(commandRegex);

    if (commands) {
        const split = message.split(commandRegex);
        innerBubble = [];
        for (let i = 0; i < split.length; i++) {
            innerBubble.push(split[i]);
            if (i < commands.length) {
                innerBubble.push(<Command key={i} command={commands[i]}/>);
            }
        }


    }
    if (!outgoing) {
        return (
            <div className="chat chat-start">
                <div className="chat-image avatar">
                    <div className="w-10 rounded-full">
                        <div className={"bg-orange-300 h-full w-full font-bold text-black justify-center flex items-center"}>BOT</div>
                    </div>
                </div>
                <div className="chat-bubble text-[var(--ifm-font-color-base-inverse)] bg-[var(--ifm-color-primary-light)]">{innerBubble}</div>
            </div>
        )
    }

    return (
        <div className="chat chat-end">
            <div className="chat-bubble bg-base-300/70 text-base-content">{innerBubble}</div>
        </div>
    )
}


export const ChatSimulator = ({updateCallback}) => {
    const inputRef = useRef(null);
    const [messages, setMessages] = useState([]);
    controller.setMessages = setMessages;
    controller.updateCallback = updateCallback;

    const onSubmit = (e) => {
        e.preventDefault();
        sendMessage(inputRef.current.value);
        inputRef.current.value = "";
        inputRef.current.focus();
    }

    useEffect(() => {
        inputRef.current.focus();
        sendMessage("/start")
    }, []);

    return (
        <div className={styles.chatContainer}>
            <div className={styles.chatHeader}>
                <div className={styles.chatHeaderTitle}>Chat Simulator</div>
            </div>
            <div className={styles.chatBody}>
                <div className={styles.chatMessagesContainer}>
                    {messages.map((message, index) => {
                        console.log(message)
                        return (
                            <ChatMessage key={index} message={message.value} outgoing={message.outgoing}/>
                        )
                    })}
                </div>
            </div>
            <form onSubmit={onSubmit} className={styles.chatFooter}>
                <input className={styles.chatInput} ref={inputRef} type="text" placeholder="Type a message"/>
                <button type="submit" className={styles.chatButton}>Send</button>
            </form>
        </div>

    )
}