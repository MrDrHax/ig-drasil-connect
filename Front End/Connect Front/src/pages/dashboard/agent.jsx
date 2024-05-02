import React from "react";
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
import { StatisticsCard, CustomerCard, Lexcard } from "@/widgets/cards";
import { RecomendationCard } from "@/widgets/cards";
// import { RecomendationsCards } from "@/widgets/cards/recomendations-card.jsx";
import {
  statisticsCardsDataAgent as statisticsCardsData,
  customerDataAgent,
  lexRecommendationData,
  messageData
} from "@/data";
import { CheckCircleIcon, ClockIcon } from "@heroicons/react/24/solid";
import {Notifications} from "../dashboard/notifications.jsx";
import { getBgColor,getTextColor, useMaterialTailwindController } from "@/context";
import ChatBox from '@/widgets/chat/chatbox.jsx';


export function Agent() {

  const controller = useMaterialTailwindController();
  const theme = controller;

  const [open, setOpen] = React.useState(1);
 
  const handleOpen = (value) => setOpen(open === value ? 0 : value);

  return (
    <div className="mt-12">
      <div className="mb-10 grid gap-y-10 gap-x-6 md:grid-cols-2 xl:grid-cols-4">
        {statisticsCardsData().map(({ icon, title, footer, ...rest }) => (
          <StatisticsCard
            key={title}
            {...rest}
            title={title}
            icon={React.createElement(icon, {
              className: "w-6 h-6 text-white",
            })}
            footer={
              <Typography className="font-normal text-blue-gray-600">
                <strong className={footer.color}>{footer.value}</strong>
                &nbsp;{footer.label}
              </Typography>
            }
          />
        ))}
      </div>

      {/*Aqui es la tarjeta importa de los datos del usuario*/}
      <div className="p-4 mb-10">
  <div className="grid grid-cols-2 gap-4">
    {customerDataAgent().map(({name, descripcion, footer, ...rest }) => (
      <CustomerCard
        key={name}
        {...rest}
        name={name}
        descripcion={descripcion}
        footer={
          <Typography className={`font-normal ${getTextColor('dark')}`}>
            <strong className={footer.color}>{footer.value}</strong>
            &nbsp;{footer.label}
          </Typography>
        }
        className="p-4 rounded-lg bg-white shadow-md"
      />
    ))}

    {lexRecommendationData().map(({recomendation, footer, ...rest }) => (
      <Lexcard
        key={recomendation}
        {...rest}
        recomendation={recomendation}
        footer={
          <Typography className={`font-normal ${getTextColor('dark')}`}>
            <strong className={footer.color}>{footer.value}</strong>
            &nbsp;{footer.label}
          </Typography>
        }
        className="p-4 rounded-lg bg-white shadow-md"
      />
    ))}
  </div>
</div>



{/*Aqui es sobre el sistema de alerta del home page */}
  <div className="mb-4 grid grid-cols-1 gap-6 xl:grid-cols-3">
    <Card className={`overflow-hidden xl:col-span-2 border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")}`}>
      <CardHeader
        floated={false}
        shadow={false}
        color="transparent"
        className="m-0 flex items-center justify-between p-6"
      >
        <div>
          <Typography variant="h6" color="blue-gray" className="mb-1">
            Alerts
          </Typography>
          <Typography
            variant="small"
            className="flex items-center gap-1 font-normal text-blue-gray-600"
          >
            <CheckCircleIcon strokeWidth={3} className="h-4 w-4 text-blue-gray-200" />
            <strong>10 alerts </strong>in this 30 minutes
          </Typography>
        </div>

        <Menu placement="left-start">
          <MenuHandler>
            <IconButton size="sm" variant="text" color="blue-gray">
              <EllipsisVerticalIcon
                strokeWidth={3}
                fill="currenColor"
                className="h-6 w-6"
              />
            </IconButton>
          </MenuHandler>
          <MenuList>
            <MenuItem>Action</MenuItem>
            <MenuItem>Another Action</MenuItem>
            <MenuItem>Something else here</MenuItem>
          </MenuList>
        </Menu>
      </CardHeader>
      <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
        <Notifications />
      </CardBody>
    </Card>


  {/* Aquí esta para cambiar el Card de recomendaciones*/}
  <Card className={`border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")}`}>
    <CardHeader
      floated={false}
      shadow={false}
      color="transparent"
      className="m-0 p-6"
    >
      <Typography variant="h6" color="blue-gray" className="mb-2">
        Recommendations
      </Typography>
      <Typography
        variant="small"
        className="flex items-center gap-1 font-normal text-blue-gray-600"
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
        openhandler={() => handleOpen(1)}/>
  <RecomendationCard 
        title={<h2>De-escalate the call</h2>} 
        content={<p>Try to calm the client and understand his situation.</p>}
        id={2}
        openID={open}
        openhandler={() => handleOpen(2)}/>
  <RecomendationCard 
        title={<h2>Average time response</h2>} 
        content={<p>Try to pay attention to incoming calls, time is valuable for our clients.</p>}
        id={3}
        openID={open}
        openhandler={() => handleOpen(3)}/>
    </CardBody>
  </Card>
  </div>

    
  {/* Aqui es para el chat del agente*/}
  <ChatBox/>

  </div>
  );
  }

export default Agent;