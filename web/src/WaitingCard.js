import { Badge, Box, Divider, Text } from 'dracula-ui';
import './WaitingCard.css';

function WaitingCard({ done }) {
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
        <Text>서울</Text>
      </Box>
      <Divider />
      <Box width="full">
        <Text>부산</Text>
      </Box>
      <Divider />
      <Box width="full">
        <Text>00.06.30.</Text>
      </Box>
      <Divider />
      <Box width="full">
        <Text>10:00~</Text>
      </Box>
      <Divider />
      <Box width="full">
        <Text>~15:00</Text>
      </Box>
      <Divider />
      <Box width="full">
        {
          done ?
          <Badge variant="outline" color="green">완료</Badge> :
          <Badge variant="outline" color="red">대기</Badge>
        }
      </Box>
    </Box>
  )
}

export default WaitingCard;
