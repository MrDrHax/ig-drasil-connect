import { Textarea, Button, IconButton, Typography, CardHeader, CardBody, CardFooter } from "@material-tailwind/react";
import { LinkIcon } from "@heroicons/react/24/outline";

import { getBgColor, getBorderColor, getTextColor, useMaterialTailwindController } from "@/context";
 
export function TwitterChatboxTextarea() {

  const controller = useMaterialTailwindController();
  const { theme } = controller;

  return (
    <div className={`flex min-w-full flex-row items-center gap-2 rounded-[99px] border ${getBorderColor("search-bar")} ${getBgColor("background-cards")} ${getTextColor("dark")} p-2`}>
      <Textarea
        rows={1}
        resize={true}
        placeholder="Your Message"
        className={`min-h-full !border-0 focus:border-transparent ${getTextColor("dark")}`}
        containerProps={{
          className: "grid h-full",
        }}
        labelProps={{
          className: "before:content-none after:content-none",
        }}
      />
      <div>
        <IconButton variant="text" className={`rounded-full ${getTextColor("dark")}`}>
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
 * @param {string} props.rol - The role of the chat message sender.
 * @return {JSX.Element} The chat message component.
 */
export function ChatMessage ({ message, rol}){
  {/* Defines the color of the card based on the role of the message sender. */}
  const isAgent = rol === 'agent';

  const controller = useMaterialTailwindController();
  const { theme } = controller;

  return (
    <div className={`flex ${isAgent ? 'justify-end' : 'justify-start'} m-5`}>
      {/* Change the color of the card based on the role of the message sender. */}
      <card className={`rounded-[100px] border  ${getBorderColor('search-bar')} ${isAgent ? getBgColor('green') : getBgColor('gray')}`}>
        <CardBody>
          <Typography color="black" className={`text-base ${getTextColor('dark')}`}>
            {message} 
          </Typography>
          <Typography  color="blue-gray" className={`text-right text-[0.7rem] g ${getTextColor('dark')}`} >
              15:30
            </Typography>
        </CardBody>

      </card>
    </div>
  );
}

export default TwitterChatboxTextarea; ChatMessage;