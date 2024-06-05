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
  ClockIcon
} from "@heroicons/react/24/solid";
import { ProfileInfoCard, MessageCard } from "@/widgets/cards";
import ChatBox from "@/widgets/chat/chatbox.jsx";
import { StatisticsChart } from "@/widgets/charts";
import { conversationsData } from "@/data";

import { getBgColor, getTextColor, getBorderColor, useMaterialTailwindController,getTypography,getTypographybold } from "@/context";
import { AgentDetails } from "@/data/agents-data";
import React, { useState, useEffect } from 'react';
import { useSearchParams } from "react-router-dom";

import {getRolesFromToken} from '@/configs/api-tools';

import {lexRecommendationData} from "@/data";

import { AgentRatingGraphData, AgentRatingData } from "@/data/supervisor-home-data";

/**
 * Renders the user profile page with tabs for app and chat views.
 *
 * @return {JSX.Element} The user profile page JSX element.
 */
export function Profile() {

  const controller = useMaterialTailwindController();
  const { theme, navColor } = controller;

  const [view, setView] = useState('app');
  const [dataToDisplay, setData] = useState([]);
  
  const [ratingData, setRatingData] = useState([]);
  const [avgRating, setAvgRating] = useState(-1);
  const [numRatings, setNumRatings] = useState(0);

  const [searchParams, setSearchParams] = useSearchParams();
  searchParams.get("profile")


  function updateData() {

    AgentDetails(searchParams.get("profile")).then((data) => {
      data.id = searchParams.get("profile");
      setData(data);
    });

    AgentRatingGraphData(searchParams.get("profile")).then((data) => {
      setRatingData(data);
    })

    AgentRatingData(searchParams.get("profile")).then((data) => {
      setAvgRating(Math.round(data[0]));
      setNumRatings(data[1]);
    })

  }

  //Call the function just once
  useEffect(() => {
    updateData();
  }, []);

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
                <Typography variant="h5" color="blue-gray" className={`text-[1.2] ${getTypography()} ${getTextColor("white3")} mb-1`}>
                  {dataToDisplay.name}
                </Typography>
                <Typography variant="small" className={`text-[0.8rem] ${getTypography()} ${getTextColor("white3")} mt-1 mb-1`}>
                {/* Role List */}
                  { getRolesFromToken().includes('manager') && getRolesFromToken().includes('agent') ? 'Agent / Supervisor' : 
                  !getRolesFromToken().includes('manager') ? 'Agent' :
                  !getRolesFromToken().includes('agent') ? 'Supervisor' : ''}

                </Typography>
                <div className="flex items-center gap-2 font-bold text-blue-gray-500">
                  {/* Rating is not loaded until the data is loaded */}
                  { avgRating == -1 ? null : <Rating value={avgRating} readonly /> }

                  <Typography color="blue-gray" className={`text-[1rem] ${getTypography()} ${getTextColor("white3")} text-[10px]`}>
                    Based on {numRatings} analysed call{ numRatings > 1 ? 's' : ''}.
                  </Typography>
                </div>

              </div>
            </div>
            {/* Tab Navigation */}
            <div className="w-96">
              <Tabs value='app' >
                <TabsHeader>
                  <Tab value="app" onClick={() => setView('app')}>
                    <InformationCircleIcon className="-mt-1 mr-2 inline-block h-5 w-5" />
                    <span className={`${getTypography()} text-black`}>Information</span>
                  </Tab>
                  <Tab value="chat" onClick={() => setView('chat')}>
                    <ChatBubbleLeftEllipsisIcon className="-mt-0.5 mr-2 inline-block h-5 w-5" />
                    <span className={`${getTypography()} text-black`}>Message</span>
                  </Tab>
                </TabsHeader>
              </Tabs>
            </div>
          </div>
        
          {/* Profile Information */}
          { view === 'app' && (
            
            <div className="gird-cols-1 mb-12 grid gap-12 px-4 lg:grid-cols-2 xl:grid-cols-3" style={{ visibility: view === 'app' ? 'visible' : 'hidden' }}>
            <ProfileInfoCard
              title="Agent AI/n Recommendations"
              description= {"Al/n, your virtual assistant recommends: " + lexRecommendationData()[0].recomendation}
              // "Hi, I'm Alec Thompson, Decisions: If you can't decide, the answer is no. If two equally difficult paths, choose the one more painful in the short term (pain avoidance is creating an illusion of equality)."
              details={{
                "name": dataToDisplay.name,
                mobile: dataToDisplay.mobile,
                email: dataToDisplay.email,

                /* Change Social Media Icons to proficiencies */
                /*
                "social media": (
                  <div className="flex items-center gap-4">
                    <i className="fa-brands fa-facebook text-blue-700" />
                    <i className="fa-brands fa-twitter text-blue-400" />
                    <i className="fa-brands fa-instagram text-purple-500" />
                  </div>
                ),
                */
                
              }}
            />
            <div>
              <Typography variant="small" className={`text-[0.8rem] ${getTypographybold()} ${getTextColor("dark")} pb-5`}>
                  Last customer calls
                </Typography>
                <ul className={`flex flex-col gap-6`}>
                  {conversationsData.map((props) => (
                    <MessageCard
                      key={props.name}
                      {...props}
                    />
                  ))}
                </ul>
              </div>

            {/* Add Average Rating Over Months Chart */}
              <div>
                <Typography /*variant="h6"*/ color="blue-gray" className={`font-normal text-[1.3rem] ${getTextColor("dark")}`}>
                  Average rating over time
                </Typography>
                { ratingData.length == 0 ?
                /* Renders a loading indicator while the data is being fetched */
                  <tr key="loading">
                    <td className="py-3 px-5 border-b border-blue-gray-50 text-center" colSpan="5">
                        <span className="flex justify-center items-center">
                            <span className={"animate-spin rounded-full h-32 w-32 border-t-2 border-b-2" + getBorderColor(navColor)}></span>
                        </span>
                    </td>
                  </tr> : 
                /* Renders the rating chart from the API call */
                ratingData.map((props) => (
                  //statisticsChartsData.map((props) => (
                  <StatisticsChart
                    key={props.title}
                    {...props}
                    footer={
                      <Typography
                        //variant="small"
                        className={`flex items-center text-base ${getTypography()}  ${getTextColor('dark')}`}
                      >
                        <ClockIcon strokeWidth={2} className={`h-4 w-4 text-blue-gray-400`} />
                        &nbsp;{props.footer}
                      </Typography>
                    }
                  />
                ))}
              </div>
            </div>
          )}
            
          {/* Chat Content */}
          {
            view === 'chat' && (
            <div className="gird-cols-1 mb-12 grid gap-12 px-4" style={{ visibility: view === 'chat' ? 'visible' : 'hidden' }}>
              <ChatBox agent_id={dataToDisplay.id} is_supervisor={true}/>
            </div>
          )}
        </CardBody>
      </Card>
    </>
  );
}

export default Profile;
