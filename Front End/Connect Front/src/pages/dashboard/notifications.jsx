import React , { useState, useEffect } from "react";
import {
  Typography,
  Card,
  CardHeader,
  CardBody,
  IconButton,
  Menu,
  MenuHandler,
  MenuList,
  MenuItem,
  Alert
} from "@material-tailwind/react";
import {EllipsisVerticalIcon} from "@heroicons/react/24/outline";
import { InformationCircleIcon } from "@heroicons/react/24/outline";
import { MessageCard } from "@/widgets/cards";
import {Alerts} from "@/data/supervisor-home-data.js"
import { getBgColor, getTextColor, useMaterialTailwindController, getTypography,getTypographybold } from "@/context";
import { CheckCircleIcon, ClockIcon, ArrowUpIcon, BookOpenIcon, UserGroupIcon} from "@heroicons/react/24/solid";
import { number } from "prop-types";


export function Notifications({is_supervisor, agent_id}) {
  const controller = useMaterialTailwindController();
  const theme = controller;
  const [info, setInfo] = useState([]);

  function updateData() {
    Alerts(is_supervisor,agent_id).then((data) => {
      setInfo(data);
    }
    );
  }

  //Call the function to recieve data just once
  useEffect(() => {
    updateData();
  }, []);

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
          {info.map(({Text,TextRecommendation,color, timestamp })=> (
            <Alert
              key={color}
              open={showAlerts[color]}
              color={color}
              onClose={() => setShowAlerts((current) => ({ ...current, [color]: false }))}
            >
              <span className={ `${getTypography()}  ${getTextColor("white")}` }>{Text}
              <br /><span className={ `${getTypographybold()} ${getTextColor("white")}` }>Recommendation: </span>{TextRecommendation} </span>
              <Typography className={ `${getTypography()}  ${getTextColor("white")} text-[0.7rem] text-right`}>{timestamp}</Typography>
            </Alert>
          ))}

    </div>
  );
}

export function NotificationsCard({is_supervisor, agent_id}) {
  const controller = useMaterialTailwindController();
  const theme = controller;
  const [numberalerts, setNumberAlerts] = useState(0);

  function updateData() {
    Alerts(is_supervisor,agent_id).then((data) => {
      setNumberAlerts(data.length);
    }
    );
  }

  //Call the function to recieve data just once
  useEffect(() => {
    updateData();
  }, []);

  return (
    <Card className={`overflow-hidden xl:col-span-2 border border-blue-gray-100 shadow-sm ${getTypography()} ${getBgColor("background-cards")}`}>
          <CardHeader
            floated={false}
            shadow={false}
            color="transparent"
            className="m-0 flex items-center justify-between p-6"
          >
            <div>
              <Typography variant="h6" color="blue-gray" className={`mb-1 text-xl ${getTypography()} ${getTextColor('dark')}`}>
                Alerts
              </Typography>
              <Typography
                //variant="small"
                className={`flex items-center gap-1 text-base ${getTypography()}  text-blue-gray-600` }
              >
                <CheckCircleIcon strokeWidth={3} className="h-4 w-4 text-blue-gray-200" />
                <strong>{numberalerts} alerts </strong>
              </Typography>
            </div>
          </CardHeader>
          <CardBody className="overflow-y-scroll px-0 pt-0 pb-2">
            <Notifications is_supervisor={is_supervisor} agent_id={agent_id} />
          </CardBody>
        </Card>
  );
}


export default NotificationsCard;
