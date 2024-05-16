import {
  HomeIcon,
  UserCircleIcon,
  TableCellsIcon,
  InformationCircleIcon,
  ServerStackIcon,
  RectangleStackIcon,
  CircleStackIcon,
  QueueListIcon,
} from "@heroicons/react/24/solid";
import { Home, Profile, Tables, Notifications, Agent } from "@/pages/dashboard";
import { SignIn, SignUp } from "@/pages/auth";

import { Teams } from "@/pages/dashboard/teams"
import { Queues } from "@/pages/dashboard/queues";


const icon = {
  className: "w-5 h-5 text-inherit",
};

export const routes = [
  {
    layout: "dashboard",
    pages: [
      {
        icon: <HomeIcon {...icon} />,
        name: "dashboard",
        path: "/home",
        element: <Home />,
      },
      {
        icon: <UserCircleIcon {...icon} />,
        name: "profile",
        path: "/profile",
        element: <Profile />,
      },
      {
        icon: <TableCellsIcon {...icon} />,
        name: "tables",
        path: "/tables",
        element: <Tables />,
      },
      {
        icon: <InformationCircleIcon {...icon} />,
        name: "notifications",
        path: "/notifications",
        element: <Notifications />,
      },
      {
        icon: <InformationCircleIcon {...icon} />,
        name: "team",
        path: "/team",
        element: <Teams />,
      },
      {
        icon: <QueueListIcon {...icon} />,
        name: "queues",
        path: "/queues",
        element: <Queues />,
      },
      {
        icon: <CircleStackIcon {...icon} />,
        name: "agent",
        path: "/agent",
        element: <Agent />,
      }
    ],
  },
  {
    title: "auth pages",
    layout: "auth",
    pages: [
      {
        icon: <ServerStackIcon {...icon} />,
        name: "sign in",
        path: "/sign-in",
        element: <SignIn />,
      },
      {
        icon: <RectangleStackIcon {...icon} />,
        name: "sign up",
        path: "/sign-up",
        element: <SignUp />,
      },
    ],
  },
];

export default routes;
