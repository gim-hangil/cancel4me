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
          <Badge variant="subtle" color="green">성공</Badge> :
          (
            running ?
            <Badge variant="subtle" color="orange">탐색 중</Badge> :
            <Badge variant="subtle" color="red">중단</Badge>
          )
        }
      </Box>
    </Box>
  );
}

export default WaitingCard;
