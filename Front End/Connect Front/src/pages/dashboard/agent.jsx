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
import { getBgColor, getTextColor, useMaterialTailwindController, getTypography, getTypographybold } from "@/context";
import ChatBox from '@/widgets/chat/chatbox.jsx';
import { AgentHomeData } from "@/data/supervisor-home-data.js";


export function Agent() {

  const controller = useMaterialTailwindController();
  const theme = controller;

  const [open, setOpen] = useState(1);

  const handleOpen = (value) => setOpen(open === value ? 0 : value);
  const [cards, setCards] = useState([]);

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

  function updateData() {

    if (sessionStorage.getItem("userID") == null) {
      AgentId().then((data) => {
        sessionStorage.setItem("userID", data);
      });
    }

    AgentHomeData(sessionStorage.getItem("userID")).then((data) => {
      setCards(data.cards);

    });
  }

  //Call the function just once
  useEffect(() => {
    updateData();
  }, []);

  return (
    <div className="mt-8">
      <div className="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-2 xl:grid-cols-4">
        {cards.map(({ icon, title, footer, ...rest }) => (
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
        ))}
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
      <div className="mb-4 grid grid-cols-1 gap-6 xl:grid-cols-3">
        <NotificationsCard is_supervisor={false} agent_id={sessionStorage.getItem("userID")} />


        {/* Recomendations Card*/}
        <Card className={`border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")}`}>
          <CardHeader
            floated={false}
            shadow={false}
            color="transparent"
            className="m-0 p-6"
          >
            <Typography /*variant="h6"*/ color="blue-gray" className={`text-lg ${getTypographybold()} ${getTextColor("white3")} text-[1.5rem] pb-1`}>
              Recommendations
            </Typography>
            <Typography
              // variant="small"
              className={`flex items-center gap-1 font-normal text-sm ${getTypography()} ${getTextColor("white3")}`}
            >
              Next, a list of recommendations for you:
            </Typography>
          </CardHeader>
          <CardBody className="pt-0">
            <RecomendationCard
              title={<h2>Check Metrics</h2>}
              content={<p>Check the client information and metrics.</p>}
              id={1}
              openID={open}
              openhandler={() => handleOpen(1)} />
            <RecomendationCard
              title={<h2>De-escalate the call</h2>}
              content={<p>Try to calm the client and understand his situation.</p>}
              id={2}
              openID={open}
              openhandler={() => handleOpen(2)} />
            <RecomendationCard
              title={<h2>Average time response</h2>}
              content={<p>Try to pay attention to incoming calls, time is valuable for our clients.</p>}
              id={3}
              openID={open}
              openhandler={() => handleOpen(3)} />
          </CardBody>
        </Card>
      </div>


      {/*Agent Chat*/}
      <ChatBox agent_id={sessionStorage.getItem("userID")} is_supervisor={false} />

    </div>
  );
}

export default Agent;