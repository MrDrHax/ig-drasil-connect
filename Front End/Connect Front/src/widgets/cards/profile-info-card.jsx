import PropTypes from "prop-types";
import {
  Card,
  CardHeader,
  CardBody,
  Typography,
} from "@material-tailwind/react";
import { getBgColor, getTextColor, useMaterialTailwindController,getTypography,getTypographybold } from "@/context";
import {ChatMessage} from "@/widgets/chat/chat.jsx";
import { data } from "autoprefixer";


export function ProfileInfoCard({ title, description, details, action, transcript }) {
  const controller = useMaterialTailwindController();

  return (
    <Card color="transparent" shadow={false}>
      <CardHeader
        color="transparent"
        shadow={false}
        floated={false}
        className="mx-0 mt-0 mb-4 flex items-center justify-between gap-4"
      >
        <Typography variant="h6" className={`${getTypography()} ${getTextColor("white3")} `}>
          {title}
        </Typography>
        {action}
      </CardHeader>
      <CardBody className="pt-0">
        {description && (
          <Typography
            //variant="small"
            className={`text-sm ${getTypography()} ${getTextColor("white3")} text-[0.8rem] `}
          >
            {description}
          </Typography>
        )}
        
        </CardBody>

        <CardBody className={`overflow-y-auto px-0 pt-0 max-h-[17rem] ` }>
        <Typography variant="h6" className={` ${getTypography()} ${getTextColor("white3")} `}>
            {transcript.length == 0 ? "No transcript available" : "Transcript"}
        </Typography>
        { transcript.length == 0 ?
          null :
          transcript.map((data) => (
          <ChatMessage message={data[1]} rol={data[0] === "AGENT" ? true: false } hour={data[2]} is_supervisor={true} />
        ))}
      </CardBody>
    </Card>
  );
}

ProfileInfoCard.defaultProps = {
  action: null,
  description: null,
  details: {},
};

ProfileInfoCard.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.node,
  details: PropTypes.object,
};

ProfileInfoCard.displayName = "/src/widgets/cards/profile-info-card.jsx";

export default ProfileInfoCard;
