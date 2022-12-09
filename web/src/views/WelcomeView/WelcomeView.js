import { Box, Card, Paragraph, Text } from 'dracula-ui';
import './WelcomeView.css';

function WelcomeView() {
  return (
    <Box className="WelcomeView">
      <Card color="purpleCyan" p="sm" m="md">
        <Text color="black">🚄 취소표라도 간절한 당신에게 기차표를 구해드립니다. 🚄</Text>
      </Card>
      <Paragraph align="left"  px="sm">
        <b>취소표가 필요해</b>는 원하는 시간대의 코레일 기차표를 대신 예매해주는 서비스입니다.
        원하는 시간대의 기차표가 매진되었을 때 취소표를 누구보다 빠르게 찾아서 예매해드립니다.
      </Paragraph>
      <Paragraph align="left" px="sm">
        예매 탭에서 원하는 일정을 입력하시면 대기열에 등록되고, 취소표가 생기면 차례로 배정됩니다.
      </Paragraph>
    </Box>
  );
}

export default WelcomeView;
