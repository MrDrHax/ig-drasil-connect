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

import { getBgColor, getTextColor, getBorderColor, useMaterialTailwindController,getTypography,getTypographybold } from "@/context";

import { AgentDetails, getAgentTranscriptSummaryData, AgentSummary } from "@/data/agents-data";

import React, { useState, useEffect } from 'react';
import { useSearchParams } from "react-router-dom";

import { lexRecommendationData } from "@/data";

import { AgentRatingGraphData, AgentRatingData, AgentConversations } from "@/data/supervisor-home-data";

/**
 * Renders the user profile page with tabs for app and chat views.
 *
 * @return {JSX.Element} The user profile page JSX element.
 */
export function Profile() {

  const [controller, dispatch] = useMaterialTailwindController();
  const { theme, navColor } = controller;

  const [view, setView] = useState('app');
  const [dataToDisplay, setData] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);
  
  const [ratingData, setRatingData] = useState([]);
  const [avgRating, setAvgRating] = useState(-1);
  const [numRatings, setNumRatings] = useState(0);
  const [avgRatingFloat, setAvgRatingFloat] = useState(0.0);

  const [conversations, setConversations] = useState([]);
  const [transcripts, setTranscripts] = useState([{}]);

  const [searchParams, setSearchParams] = useSearchParams();
  searchParams.get("profile")


  const [aiRecommendations, setAiRecommendations] = useState("<p>Fetching data...</p>");

  function getAiRecommendations() {
    AgentSummary(searchParams.get("profile")).then((data) => {
      console.log(data);
      setAiRecommendations(data["content"]);
    }).catch(() => {
      setAiRecommendations("<p>Al.n is not available at the moment. Try again later</p>");
    });
  }

  function updateData() {

    AgentDetails(searchParams.get("profile")).then((data) => {
      data.id = searchParams.get("profile");
      setData(data);
    });

    AgentRatingGraphData(searchParams.get("profile")).then((data) => {
      setRatingData(data);
    })

    AgentRatingData(searchParams.get("profile")).then((data) => {
      setAvgRatingFloat(data[0]);
      setAvgRating(Math.round(data[0]));
      setNumRatings(data[1]);
    })

    AgentConversations(searchParams.get("profile")).then((data) => {
      setConversations(data);
    })

    setIsLoaded(true);

    getAiRecommendations();

    getAgentTranscriptSummaryData(searchParams.get("profile")).then((data) => {
      setTranscripts(data);
      setIsLoaded(true);
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
                  { dataToDisplay.roles == null ? '' : 
                  dataToDisplay.roles.includes('Admin') ? 'Agent / Supervisor' : 
                  dataToDisplay.roles.includes('Agent') ? 'Agent' :
                  dataToDisplay.roles.includes('CallCenterManager') ? 'Supervisor' : ''}

                </Typography>
                <div className="flex items-center gap-2 font-bold text-blue-gray-500">
                  {/* Rating is not loaded until the data is loaded */}
                  { avgRating == -1 ? null : <Rating value={avgRating} readonly /> }

                  <Typography className={`${getTypography()} ${getTextColor("white3")} text-[16px]`}>
                    {avgRatingFloat.toFixed(1)}
                  </Typography>
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
            { !isLoaded ?
                <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
                <span className="flex justify-center items-center">
                <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
                </span>
              </div> :
            <ProfileInfoCard
              title="Agent Al.n Recommendations"
                description={<div dangerouslySetInnerHTML={{ __html: aiRecommendations }} />}
              details={{
                "Name": dataToDisplay.name,
                "Mobile Phone": dataToDisplay.mobile,
                "Email": dataToDisplay.email,
              }}
              transcript={transcripts}
            />
            }

              {/* Add Last Customer Calls */}
              <div>
              <Typography variant="small" className={`text-[0.8rem] ${getTypographybold()} ${getTextColor("dark")} pb-5`}>
                  Last customer calls
                </Typography>
                <ul className={`flex flex-col gap-6 max-h-[20rem] overflow-auto`}>
                  { conversations.length == 0 ?
                  (
                    <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
                    <span className="flex justify-center items-center">
                    <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
                    </span>
                    <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
                        Conversations are now loading...
                    </Typography>
                    </div>
                    ) :
                  conversations.map((props) => (
                    <MessageCard
                      key={props.timestamp}
                      img="/img/favicon.png"
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
                (
                  <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
                  <span className="flex justify-center items-center">
                  <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
                  </span>
                  <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
                      Graph is now loading...
                  </Typography>
                  </div>
                  ) : 
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
