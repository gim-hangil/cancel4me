import { Box } from 'dracula-ui';
import WaitingCard from './WaitingCard';
import './WaitingView.css';

function WaitingView() {
  return (
    <Box className="WaitingView">
      <WaitingCard done={true} />
      <WaitingCard done={false} />
      <WaitingCard done={false} />
    </Box>
  );
}

export default WaitingView;
