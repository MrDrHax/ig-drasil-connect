import PropTypes from "prop-types";
import {
  Card,
  CardHeader,
  CardBody,
  Typography,
} from "@material-tailwind/react";
import { getBgColor, getTextColor, useMaterialTailwindController,getTypography,getTypographybold } from "@/context";


export function ProfileInfoCard({ title, description, details, action }) {
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
      <CardBody className="p-0">
        {description && (
          <Typography
            //variant="small"
            className={`text-sm ${getTypography()} ${getTextColor("white3")} text-[0.8rem] `}
          >
            {description}
          </Typography>
        )}
        {description && details ? (
          <hr className="my-8 border-blue-gray-50" />
        ) : null}
        {details && (
          <ul className="flex flex-col gap-4 p-0">
            {Object.keys(details).map((el, key) => (
              <li key={key} className="flex items-center gap-4">
                <Typography
                  //variant="small"
                  color="blue-gray"
                  className={`text-sm ${getTypographybold()} ${getTextColor("white3")} text-[0.8rem] `}
                >
                  {el}:
                </Typography>
                {typeof details[el] === "string" ? (
                  <Typography
                    //variant="small"
                    className={`text-sm ${getTypography()} ${getTextColor("white3")} text-[0.6rem] `}
                  >
                    {details[el]}
                  </Typography>
                ) : (
                  details[el]
                )}
              </li>
            ))}
          </ul>
        )}
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
