import React from "react";
import {
  Typography,
  Card,
  CardHeader,
  CardBody
} from "@material-tailwind/react";

import {
  messageData, getChatData
} from "@/data";
import { getBgColor, getTextColor, useMaterialTailwindController,getTypographybold } from "@/context";
import {TwitterChatboxTextarea ,ChatMessage} from "@/widgets/chat";

import {useState, useEffect} from 'react';

/**
 * Renders a chat box component.
 *
 * @return {JSX.Element} The chat box component.
 */
export function ChatBox({agent_id, is_supervisor}) {
    const controller = useMaterialTailwindController();
    const { theme } = controller;

    const [dataToDisplay, setData] = useState([]);


    function updateData() {

        getChatData(agent_id).then((data) => {
          setData(data);
        });
      }
    
      //Call the function just once
      useEffect(() => {
        updateData();
      }, []);

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
            <CardBody className={`overflow-y-scroll border border-${getTextColor("dark")} px-0 pt-0 pb-2 ` } style={{ maxHeight: '400px'}} >
            
                {/* Renders the chat messages from the API calls */}
                {dataToDisplay.map(({ content, supervisor_sender, timestamp }) => (
                    <ChatMessage message={content} rol={supervisor_sender} hour={timestamp} is_supervisor={is_supervisor}/>
                ))}

            {/* Renders the chat messages from a Hard-coded array.
            {messageData.map(({ message, rol, hour }) => (
                <ChatMessage message={message} rol={rol} hour={hour} />
            ))}
            */}

            </CardBody>
            <CardBody className="p-4">
                <TwitterChatboxTextarea agent_id={agent_id} is_supervisor={is_supervisor}/>
            </CardBody>
        </Card>
    );
}



export default ChatBox; 