import {
  Card,
  CardBody,
  CardHeader,
  CardFooter,
  Avatar,
  Typography,
  Tabs,
  TabsHeader,
  Tab,
  Switch,
  Tooltip,
  Button,
  TabPanel,
  Rating,
} from "@material-tailwind/react";
import {
  InformationCircleIcon,
  ChatBubbleLeftEllipsisIcon,
  Cog6ToothIcon,
  PencilIcon,
} from "@heroicons/react/24/solid";
import { Link } from "react-router-dom";
import { ProfileInfoCard, MessageCard } from "@/widgets/cards";
import ChatBoxSupervisor from "@/widgets/chat/chatboxsuper";
import { StatisticsChart } from "@/widgets/charts";
import { platformSettingsData, conversationsData, projectsData, statisticsChartsData } from "@/data";


import { getBgColor, getTextColor, useMaterialTailwindController } from "@/context";
import { AgentDetails } from "@/data/agents-data";
import React, { useEffect, useState } from 'react';


/**
 * Renders the user profile page with tabs for app and chat views.
 *
 * @return {JSX.Element} The user profile page JSX element.
 */
export function Profile() {

  const controller = useMaterialTailwindController();

  const [view, setView] = useState('app');

  
  /*const [dataToDisplay, setData] = useState([]);

  function updateData()
  {
    AgentDetails(id).then((data) => {
      setData(data.data);
    }).catch((error) => {
      console.error(error);
    });
  } */

  return (
    <>    
      <Card className={`mx-3 mb-6 lg:mx-4 border border-blue-gray-100 ${getTextColor("dark")} ${getBgColor("background-cards")}`}>
        <CardBody className="p-4">
          {/* Header */}
          <div className="mb-10 flex items-center justify-between flex-wrap gap-6">
            <div className="flex items-center gap-6">
              <Avatar
                src="/img/user_test.png" //placeholder avatar icon
                alt="bruce-mars"
                size="xl"
                variant="rounded"
                className="rounded-lg shadow-lg shadow-blue-gray-500/40"
              />
              <div>
                <Typography variant="h5" color="blue-gray" className="mb-1">
                  Unknown
                </Typography>
                <Typography variant="small" className="font-normal text-blue-gray-600">
                  Agent
                </Typography>
                <div className="flex items-center gap-2 font-bold text-blue-gray-500">
              <Rating value={5} readonly/>
              <Typography color="blue-gray" className="font-medium text-blue-gray-500">
                Based on 12 customer Reviews.
              </Typography>
              </div>

              </div>
            </div>
            {/* Tab Navigation */}
            <div className="w-96">
              <Tabs value='app'>
                <TabsHeader>
                  <Tab value="app" onClick={() => setView('app')}>
                    <InformationCircleIcon className="-mt-1 mr-2 inline-block h-5 w-5" />
                    Information
                  </Tab>
                  <Tab value="chat" onClick={() => setView('chat')}>
                    <ChatBubbleLeftEllipsisIcon className="-mt-0.5 mr-2 inline-block h-5 w-5" />
                    Message
                  </Tab>
                </TabsHeader>
              </Tabs>
            </div>
          </div>
        
          <div className="gird-cols-1 mb-12 grid gap-12 px-4 lg:grid-cols-2 xl:grid-cols-3">
            <ProfileInfoCard
              title="About agent"
              description="Hi, I'm Alec Thompson, Decisions: If you can't decide, the answer is no. If two equally difficult paths, choose the one more painful in the short term (pain avoidance is creating an illusion of equality)."
              details={{
                "name": "Alec M. Thompson",
                mobile: "(44) 123 1234 123",
                email: "alecthompson@mail.com",
                proficiencies: (
                  <div className="flex items-center gap-4">
                    <i className="fa-brands fa-facebook text-blue-700" />
                    <i className="fa-brands fa-twitter text-blue-400" />
                    <i className="fa-brands fa-instagram text-purple-500" />
                  </div>
                ),
              }}
              action={
                <Tooltip content="Edit Profile">
                  <PencilIcon className={`h-4 w-4 cursor-pointer ${getTextColor("dark")}`} />
                </Tooltip>
              }
            />
            <div>
              <Typography variant="small" className={`font-normal ${getTextColor("dark")}`}>
                  Last customer calls
                </Typography>
                <ul className="flex flex-col gap-6">
                  {conversationsData.map((props) => (
                    <MessageCard
                      key={props.name}
                      {...props}
                      action={
                        <Button variant="text" size="sm">
                          reply
                        </Button>
                      }
                    />
                  ))}
                </ul>
              </div>
            </div>

            {/* Add Average Rating Over Months Chart */}
            <div>
              <Typography variant="h6" color="blue-gray" className={`font-normal ${getTextColor("dark")}`}>
                Average rating over months
              </Typography>
              <StatisticsChart chart={statisticsChartsData[3].chart} /> {/* Pass the chart object */}
            </div>
            
          {/* Chat Content */}
          {
            view === 'chat' && (
            <div className="gird-cols-1 mb-12 grid gap-12 px-4" style={{ visibility: view === 'chat' ? 'visible' : 'hidden' }}>
              <ChatBoxSupervisor/>
            </div>
          )}
        </CardBody>
      </Card>
    </>
  );
}

export default Profile;
