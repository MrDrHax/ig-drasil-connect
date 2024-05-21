import PropTypes from "prop-types";
import { Avatar, Typography } from "@material-tailwind/react";
import { getBgColor, getTextColor, useMaterialTailwindController,getTypography,getTypographybold } from "@/context";

export function MessageCard({ img, name, message, action }) {
  const controller = useMaterialTailwindController();

  return (
    <div className="flex items-center justify-between gap-4">
      <div className="flex items-center gap-4">
        <Avatar
          src={img}
          alt={name}
          variant="rounded"
          className="shadow-lg shadow-blue-gray-500/25"
        />
        <div>
          <Typography
            //variant="small"
            className={`text-sm ${getTypographybold()} ${getTextColor("white3")} text-[0.8rem]`}
          >
            {name}
          </Typography>
          <Typography className={`text-[1rem] ${getTypography()} ${getTextColor("white3")} text-[0.6rem]`}>
            {message}
          </Typography>
        </div>
      </div>
      {action}
    </div>
  );
}

MessageCard.defaultProps = {
  action: null,
};

MessageCard.propTypes = {
  img: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  message: PropTypes.node.isRequired,
  action: PropTypes.node,
};

MessageCard.displayName = "/src/widgets/cards/message-card.jsx";

export default MessageCard;
