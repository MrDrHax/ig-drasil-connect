import React from "react";
import {
  Typography,
  Alert,
  Card,
  CardHeader,
  CardBody,
} from "@material-tailwind/react";
import { InformationCircleIcon } from "@heroicons/react/24/outline";
import { MessageCard } from "@/widgets/cards";

export function Notifications() {
  const [showAlerts, setShowAlerts] = React.useState({
    blue: true,
    green: true,
    orange: true,
    red: true,
  });
  const [showAlertsWithIcon, setShowAlertsWithIcon] = React.useState({
    blue: true,
    green: true,
    orange: true,
    red: true,
  });
  const alerts = ["gray", "green", "orange", "red"];
  {/* Creacion de las alertas
    mx-auto: margin horizontal automatico
    px-7: padding horizontal 7
    my-5: margin vertical 5
*/}
  return (
    <div className="mx-auto px-7 my-5 flex max-w-screen-lg flex-col gap-7 ">
          {alerts.map((color) => (
            <Alert
              key={color}
              open={showAlerts[color]}
              color={color}
              onClose={() => setShowAlerts((current) => ({ ...current, [color]: false }))}
            >
              {color === "gray" && (
                <span>This is an information alert message.</span>
              )}
              {color === "green" && (
                <span>This is a logs alert message.</span>
              )}
              {color === "orange" && (
                <span>This is an agent alert message.</span>
              )}
              {color === "red" && (
                <span>This is an issue call alert message.</span>
              )}
              
            </Alert>
          ))}

     {/*
     |<Card>
     <CardHeader
       color="transparent"
       floated={false}
       shadow={false}
       className="m-0 p-4"
     >
       <Typography variant="h5" color="blue-gray">
         Alerts with Icon
       </Typography>
     </CardHeader>
     <CardBody className="flex flex-col gap-4 p-4">
       {alerts.map((color) => (
         <Alert
           key={color}
           open={showAlertsWithIcon[color]}
           color={color}
           icon={
             <InformationCircleIcon strokeWidth={2} className="h-6 w-6" />
           }
           onClose={() => setShowAlertsWithIcon((current) => ({
             ...current,
             [color]: false,
           }))}
         >
           A simple {color} alert with an <a href="#">example link</a>. Give
           it a click if you like.
         </Alert>
       ))}
     </CardBody>
   </Card>
   <MessageCard>
        <Typography variant="h5" color="blue-gray">
          Message Card
        </Typography>
        <Typography variant="body" color="blue-gray">
          This is a message card. It is used to display messages to the user.
        </Typography>
      </MessageCard>
      */} 
      

    </div>
  );
}

export default Notifications;
