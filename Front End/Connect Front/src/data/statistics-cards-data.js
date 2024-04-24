import {
  UserGroupIcon,
  UserCircleIcon,
  ClockIcon,
  ChartBarIcon,
} from "@heroicons/react/24/solid";

export function statisticsCardsData() {
  console.warn("statisticsCardsData is not yet done")
  return [
    {
      color: "purple",
      icon: UserGroupIcon,
      title: "Connected users",
      value: "80",
      footer: {
        color: "text-green-500",
        value: "+32",
        label: "than today's average",
      },
    },
    {
      color: "gray",
      icon: UserCircleIcon,
      title: "Connected agents",
      value: "10",
      footer: {
        color: "text-gray-500",
        value: "4",
        label: "offline",
      },
    },
    {
      color: "red",
      icon: ChartBarIcon,
      title: "Capacity",
      value: "50%",
      footer: {
        color: "text-green-500",
        value: "+3%",
        label: "expected in the next hour",
      },
    },
    {
      color: "blue",
      icon: ClockIcon,
      title: "Average call time",
      value: "5:23",
      footer: {
        color: "text-red-500",
        value: "+23s",
        label: "than expected",
      },
    },
  ];
}

export function statisticsCardsDataAgent() {
  console.warn("statisticsCardsData is not yet done")
  return [
    {
      color: "green",
      icon: UserGroupIcon,
      title: "people to answer",
      value: "80",
      footer: {
        color: "text-green-500",
        value: "+32",
        label: "than today's average",
      },
    },
    {
      color: "gray",
      icon: UserCircleIcon,
      title: "productive time",
      value: "6h 30m",
      footer: {
        color: "text-green-500",
        value: "+20",
        label: "than expected",
      },
    },
    {
      color: "red",
      icon: ChartBarIcon,
      title: "Rakind",
      value: "75%",
      footer: {
        color: "text-red-500",
        value: "-3%",
        label: "than expected",
      },
    },
    {
      color: "blue",
      icon: ClockIcon,
      title: "Average call time",
      value: "5:23",
      footer: {
        color: "text-red-500",
        value: "+23s",
        label: "than expected",
      },
    },
  ];
}

export default statisticsCardsData; statisticsCardsDataAgent;