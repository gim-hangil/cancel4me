import { Badge, Box, Divider, Text } from 'dracula-ui';
import './WaitingCard.css';

function WaitingCard({
  departure_station,
  arrival_station,
  date,
  departure_base,
  arrival_limit,
  id,
  reserved,
  running
}) {
  return (
    <Box
      className="WaitingCard"
      color="blackSecondary"
      rounded="lg"
      display="flex"
      m="xxs"
      p="xss"
    >
      <Box width="full">
        <Text>{ departure_station }</Text>
      </Box>
      <Divider />
      <Box width="full">
        <Text>{ arrival_station }</Text>
      </Box>
      <Divider />
      <Box width="full">
        <Text>{ date }</Text>
      </Box>
      <Divider />
      <Box width="full">
        <Text>{ departure_base }~</Text>
      </Box>
      <Divider />
      <Box width="full">
        <Text>~{ arrival_limit }</Text>
      </Box>
      <Divider />
      <Box width="full">
        {
          reserved ?
          <Badge variant="outline" color="green">완료</Badge> :
          <Badge variant="outline" color="red">대기</Badge>
        }
      </Box>
    </Box>
  );
}

export default WaitingCard;
