import React from "react";
import {
  Typography,
  Card,
  CardHeader,
  CardBody
} from "@material-tailwind/react";

import {
  messageData, getChatData, AgentId
} from "@/data";
import { getBgColor, getTextColor, getBorderColor,getTypography, useMaterialTailwindController,getTypographybold } from "@/context";
import {TwitterChatboxTextarea ,ChatMessage} from "@/widgets/chat";

import {useState, useEffect, useRef} from 'react';

/**
 * Renders a chat box component.
 *
 * @return {JSX.Element} The chat box component.
 */
export function ChatBox({agent_id, is_supervisor}) {
    const [controller, dispatch] = useMaterialTailwindController();
    const { navColor, theme } = controller;

    const [dataToDisplay, setData] = useState([]);
    const [isLoaded, setIsLoaded] = useState(false);

    const containerRef = useRef(null);

    function updateData() {
        setIsLoaded(false);
        getChatData(agent_id).then((data) => {
          setData(data);
          setIsLoaded(true);
        });
      }

    const scrollToBottom = () => {
      if (containerRef.current)
        containerRef.current.scrollTop = containerRef.current.scrollHeight;
    };
    
      //Call the function just once
      useEffect(() => {
        updateData();
        scrollToBottom();
      }, [agent_id]);

    return (
        <Card className={`overflow-hidden xl:col-span-2 border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")} `} >
            <CardHeader
            floated={false}
            shadow={false}
            color="transparent"
            className="m-0 flex items-center justify-between p-6"
            >
                <div>
                    <Typography variant="h6" color="blue-gray" className={`mb-1 ${getTypographybold()} ${getTextColor("dark")}`}>
                    Chat
                    </Typography>
                </div>
            </CardHeader>
            <CardBody ref={containerRef} className={`overflow-y-auto border border-${getTextColor("dark")} px-0 pt-0 pb-2 ` } style={{ maxHeight: '400px'}} >
            
                {!isLoaded || agent_id === null ?
                /* Renders a loading indicator while the data is being fetched */
                <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
                <span className="flex justify-center items-center">
                <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
                </span>
                <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
                    Chat is now loading...
                </Typography>
                </div>
                /* Renders the chat messages from the API calls */
                : dataToDisplay.map(({ content, supervisor_sender, timestamp }) => (
                    <ChatMessage message={content} rol={supervisor_sender} hour={timestamp} is_supervisor={is_supervisor}/>
                ))}

            </CardBody>
            <CardBody className="p-4">
                <TwitterChatboxTextarea agent_id={agent_id} is_supervisor={is_supervisor}/>
            </CardBody>
        </Card>
    );
}



export default ChatBox; 