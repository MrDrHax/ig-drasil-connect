import React from "react";
import {
  Typography,
  Card,
  CardHeader,
  CardBody
} from "@material-tailwind/react";

import {
  messageData
} from "@/data";
import { getBgColor, getTextColor, useMaterialTailwindController } from "@/context";
import {TwitterChatboxTextarea ,ChatMessage } from "@/widgets/chat";

/**
 * Renders a chat box component.
 *
 * @return {JSX.Element} The chat box component.
 */
export function ChatBox() {
    const controller = useMaterialTailwindController();
    const { theme } = controller;

    return (
        <Card className={`overflow-hidden xl:col-span-2 border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")}`}>
            <CardHeader
            floated={false}
            shadow={false}
            color="transparent"
            className="m-0 flex items-center justify-between p-6"
            >
                <div>
                    <Typography variant="h6" color="blue-gray" className={`mb-1 ${getTextColor("dark")}`}>
                    Chat
                    </Typography>
                </div>
            </CardHeader>
            <CardBody className="overflow-y-scroll border border-blue-gray-100 px-0 pt-0 pb-2 " style={{ maxHeight: '400px'}}>
            {messageData.map(({ message, rol }) => (
                <ChatMessage message={message} rol={rol} />
            ))}

            </CardBody>
            <CardBody className="p-4">
                <TwitterChatboxTextarea />
            </CardBody>
        </Card>
    );
}

export default ChatBox;