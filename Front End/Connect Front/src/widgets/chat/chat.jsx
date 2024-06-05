import { Textarea, Button, IconButton, Typography, CardHeader, Card, CardBody, CardFooter } from "@material-tailwind/react";
import { LinkIcon } from "@heroicons/react/24/outline";

import { getBgColor, getBorderColor, getTextColor, useMaterialTailwindController,getTypography,getTypographybold } from "@/context";

import { postMessageData } from "@/data";
import { useEffect, useState } from "react";
 
/**
 * Renders a textarea component with a send button for posting messages.
 *
 * @param {Object} props - The properties object.
 * @param {string} props.agent_id - The ID of the agent.
 * @param {boolean} props.is_supervisor - Whether the message is from the supervisor.
 * @return {JSX.Element} The rendered textarea component.
 */
export function TwitterChatboxTextarea({agent_id, is_supervisor}) {

  const controller = useMaterialTailwindController();
  const { theme } = controller;

  const [message, setMessage] = useState("");

  const handleChange = (event) => {
    setMessage(event.target.value);
  };

  function clickSend() {
    postMessageData(agent_id, message, is_supervisor);
    setMessage("");
  }

  return (
    <div className={`flex min-w-full flex-row items-center gap-2 rounded-[99px] border ${getBorderColor("search-bar")} ${getBgColor("background-cards")} ${getTextColor("dark")} p-2`}>
      <Textarea
        value={message}
        onChange={handleChange}
        rows={1}
        resize={true}
        placeholder="Your Message"
        className={`min-h-full !border-0 focus:border-transparent ${getTextColor("dark")} `}
        containerProps={{
          className: "grid h-full",
        }}
        labelProps={{
          className: "before:content-none after:content-none",
        }}
      />
      <div>
        <IconButton onClick={() => clickSend()} variant="text" className={`rounded-full ${getTextColor("dark")}`}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
            className="h-5 w-5"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
            />
          </svg>
        </IconButton>
      </div>
    </div>
  );
}

/**
 * Renders a chat message component.
 *
 * @param {Object} props - The properties of the chat message.
 * @param {string} props.message - The content of the chat message.
 * @param {boolean} props.rol - Whether the message is from a supervisor
 * @param {string} props.hour - The timestamp of the chat message.
 * @param {boolean} props.is_supervisor - Whether the current viewer is a supervisor.
 * @return {JSX.Element} The chat message component.
 */
export function ChatMessage ({ message, rol, hour, is_supervisor }) {
  {/* Defines the color of the card based on the role of the message sender. */}
  const isAgent = rol === is_supervisor;

  const controller = useMaterialTailwindController();
  const { theme } = controller;

  return (
     <div className={`flex ${isAgent ? 'justify-end' : 'justify-start'} m-5`}>
        {/* Change the color of the card based on the role of the message sender. */}
        <Card className={`m-2 rounded-[100px] border  ${getBorderColor('search-bar')} ${isAgent ? getBgColor('green') : getBgColor('gray')}`}  style={{ wordWrap: 'break-word', overflowWrap: 'break-word', maxWidth: '300px' }}>
          <CardBody>
          <Typography color="black" className={`text-base ${getTypography()} ${isAgent ? getTextColor("white2") : getTextColor("black")}`}>
              {message} 
            </Typography>
            <Typography  color="blue-gray" className={`text-right text-[0.7rem] g ${getTypography()} ${isAgent ? getTextColor("white2") : getTextColor("black")} `} >
                
                {hour.split("T")[0]} {hour.split("T")[1].split(".")[0].split(":")[0]}:{hour.split("T")[1].split(".")[0].split(":")[1]}
              </Typography>
          </CardBody>

        </Card>
      </div>
    );
  }

export default TwitterChatboxTextarea; ChatMessage;