import PropTypes from "prop-types";
import { Avatar, Typography } from "@material-tailwind/react";
import { Chip } from "@material-tailwind/react";
import { getBgColor, getTextColor, useMaterialTailwindController,getTypography,getTypographybold } from "@/context";

export function MessageCard({ img, summary, status, duration, agentSentiment, customerSentiment, timestamp}) {
  const controller = useMaterialTailwindController();

  return (
    <div className="flex items-center justify-between gap-4">
      <div className="flex items-center gap-4">
        <Avatar
          src={img}
          alt={timestamp}
          variant="circular"
          className="shadow-lg shadow-blue-gray-500/25"
        />
        <div>
          <Typography
            className={`text-sm ${getTypographybold()} ${getTextColor("white3")} text-[1rem]`}
          >
            {timestamp}
          </Typography>
          <Typography className={`text-[1rem] ${getTypography()} ${getTextColor("white3")} text-[0.8rem]`}>
            {summary}
          </Typography>

          <Typography
            className={`text-sm ${getTypographybold()} ${getTextColor("white3")} text-[0.6rem]`}
          >
            {status}
          </Typography>

          <Typography
            className={`text-sm ${getTypography()} ${getTextColor("white3")} text-[0.6rem]`}
          >
            {(duration / 60000).toFixed(0)} minutes {Math.ceil((duration / 1000).toFixed(1) % 60)} seconds
          </Typography>

          <Typography
            className={`text-sm ${getTypography()} ${agentSentiment > 1 ? "text-green-500" : agentSentiment < -1 ? "text-red-500" : getTextColor("orange")} text-[0.6rem]`}
          >
            Agent Sentiment was {agentSentiment > 1 ? "Positive" : agentSentiment < -1 ? "Negative" : "Neutral"}
          </Typography>
          <Typography
            className={`text-sm ${getTypography()} ${customerSentiment > 1 ? "text-green-500" : customerSentiment < -1 ? "text-red-500" : getTextColor("orange")} text-[0.6rem]`}
          >
            Customer Sentiment was {customerSentiment > 1 ? "Positive" : customerSentiment < -1 ? "Negative" : "Neutral"}
          </Typography>
        </div>
      </div>
    </div>
  );
}

MessageCard.displayName = "/src/widgets/cards/message-card.jsx";

export default MessageCard;
