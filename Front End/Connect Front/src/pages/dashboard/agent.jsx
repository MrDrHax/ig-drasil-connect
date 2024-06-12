import React, { useState, useEffect } from "react";
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
} from "@material-tailwind/react";
import {
  EllipsisVerticalIcon,
  CheckCircleIcon,
  ArrowUpIcon,
} from "@heroicons/react/24/outline";
import { BookOpenIcon, UserGroupIcon,StarIcon,ClockIcon, ChartBarIcon, } from "@heroicons/react/24/solid";
import { StatisticsCard, CustomerCard, Lexcard } from "@/widgets/cards";
import { RecomendationCard } from "@/widgets/cards";
// import { RecomendationsCards } from "@/widgets/cards/recomendations-card.jsx";
import {
  statisticsCardsDataAgent as statisticsCardsData,
  customerDataAgent,
  lexRecommendationData,
  messageData,
  AgentId
} from "@/data";
import { NotificationsCard } from "../dashboard/notifications.jsx";
import { getBgColor, getTextColor, useMaterialTailwindController, getTypography, getTypographybold, getBorderColor } from "@/context";
import ChatBox from '@/widgets/chat/chatbox.jsx';
import { AgentHomeData } from "@/data/supervisor-home-data.js";


export function Agent() {

  const [controller, dispatch] = useMaterialTailwindController();
  const {navColor, theme} = controller;

  const [open, setOpen] = useState(1);
  const [userID, setUserID] = useState(null);

  const handleOpen = (value) => setOpen(open === value ? 0 : value);
  const [cards, setCards] = useState([]);

  const [isLoaded, setIsLoaded] = useState(false);

  function getIcon(icon) {
    switch (icon) {
      case "Arrow":
        return ArrowUpIcon;
      case "Book":
        return BookOpenIcon;
      case "Clock":
        return ClockIcon;
      case "Person":
        return UserGroupIcon;
      case "Star":
        return StarIcon;
      case "Chart":
        return ChartBarIcon;
      default:
        return CheckCircleIcon;
    }
  }

  useEffect(() => {
    AgentId().then((data) => {
      setUserID(data);
    });
  }, []);

  useEffect(() => {
    if (userID) {
      AgentHomeData(userID).then((data) => {
        setCards(data.cards);
        setIsLoaded(true);
      });
    }
  }, [userID]);

  return (
    <div className="mt-8">

      {/*Statistics Cards*/}
      <div className="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-2 xl:grid-cols-4">
        {!isLoaded || userID == null ? (
          <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
          <span className="flex justify-center items-center">
          <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
          </span>
          <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
              Cards are now loading...
          </Typography>
          </div>
          ) : (
        cards.map(({ icon, title, footer, ...rest }) => (
          <StatisticsCard
            key={title}
            {...rest}
            title={title}
            icon={React.createElement(getIcon(icon), {
              className: "w-6 h-6 text-white",
            })}
            footer={
              <Typography className={`text-base ${getTypography()} ${getTextColor('dark')}`}>
                <strong className={footer.color}>{footer.value}</strong>
                &nbsp;{footer.label}
              </Typography>
            }
          />
        ))
        )}
      </div>

      {/*Client Data*/}
      <div className="p-4 mb-10">
        <div className="grid grid-cols-2 gap-4">
          {customerDataAgent().map(({ name, descripcion, footer, ...rest }) => (
            <CustomerCard
              key={name}
              {...rest}
              name={name}
              descripcion={descripcion}
              footer={
                <Typography className={`text-base ${getTypography()} ${getTextColor('dark')}`}>
                  <strong className={footer.color}>{footer.value}</strong>
                  &nbsp;{footer.label}
                </Typography>
              }
              className="p-4 rounded-lg bg-white shadow-md"
            />
          ))}

          {lexRecommendationData().map(({ recomendation, footer, ...rest }) => (
            <Lexcard
              key={recomendation}
              {...rest}
              recomendation={recomendation}
              footer={
                <Typography className={`text-base ${getTypography()} ${getTextColor('dark')}`}>
                  <strong className={footer.color}>{footer.value}</strong>
                  &nbsp;{footer.label}
                </Typography>
              }
              className="p-4 rounded-lg bg-white shadow-md"
            />
          ))}
        </div>
      </div>



      {/*Agent Alerts */}      
      <div id="notifications" className="mb-4 grid grid-cols-1 gap-6 xl:grid-cols-1">
        {
        userID == null ?
          <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
          <span className="flex justify-center items-center">
          <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
          </span>
          <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
              Notifications are now loading...
          </Typography>
          </div> : 
        <NotificationsCard is_supervisor={false} agent_id={userID} />
        }
      </div>

      {/*Agent Chat*/}
      { userID == null ? 
        <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
        <span className="flex justify-center items-center">
        <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
        </span>
        <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
            Chat is now loading...
        </Typography>
        </div>
      :
        <ChatBox agent_id={userID} is_supervisor={false} />
      }

    </div>
  );
}

export default Agent;