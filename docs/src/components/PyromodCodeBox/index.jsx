import {on} from "../../utils/event";
import {useState} from "react";
import clsx from "clsx";
import { CopyBlock, dracula } from 'react-code-blocks';

export const PyromodCodeBox = () => {
    const [step, setStep] = useState(0);

    on("pyromodCodeStep", (step) => {
        setStep(step);
    });
    
    const codeText = `
@Client.on_message(filters.command("start"))
    def start(client, message):
        chat = message.chat
        response = await chat.ask("Oh hey! What is your name?")
        name = response.text
        response = await chat.ask(f"Hello {name}! Please tell me your age.")
        age = response.text
        response = await chat.ask(f"So you are {age} years old. Now i wanna know your hobby. What do you like to do?")
        hobby = response.text
        await message.reply(f"Oh, i see. Okay, so your name is {name}, you are {age} years old and you like to {hobby}. Nice to meet you!")
    `.trim()

    const codeLines = codeText.split("\n");

    const translateStepToLine = (step) => {
        switch (step) {
            case 1:
                return "4"
            case 2:
                return "6"
            case 3:
                return "8"
            default:
                return ""
        }
    }

    return (
       <div className="mockup-code bg-base-200 h-96 w-[80vw] md:w-[800px] overflow-auto flex flex-col items-start scrollbar-thin scrollbar-thumb-neutral scrollbar-rounded-lg text-base">
           {codeLines.map((line, index) => {
                const lineNumber = index + 1;
                const stepLine = translateStepToLine(step);
                const highlightLine = stepLine === lineNumber.toString();

                const highlight = "bg-primary text-primary-content";
                const fade = "bg-transparent text-base-content opacity-40";
                const normal = "bg-transparent text-base-content";

                const className = "flex gap-2 rounded-none p-0 overflow-visible";
                const extraClassName = stepLine? (highlightLine? highlight: fade): normal;
                return (
                    <pre data-prefix={lineNumber} className={clsx(className, extraClassName)} key={index}><code>{line}</code></pre>
                )
           })}
       </div>
    )


}