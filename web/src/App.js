import { Box, Divider, Heading } from 'dracula-ui';
import SelectStation from './SelectStation';
import './App.css';

function App() {
  return (
    <Box className="App" width="full" mx="auto" my="xs">
      <Box className="heading" my="sm">
        <Heading>
          취소표가 필요해!
        </Heading>
      </Box>
      <Box className="station" display="flex">
        <SelectStation label="출발" />
        <SelectStation label="도착" />
      </Box>
      <Divider color="purple" mx="xs" my="sm" />
    </Box>
  );
}

export default App;
