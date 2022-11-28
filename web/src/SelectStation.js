import { Card, Select, Text } from 'dracula-ui';
import './SelectStation.css';

function SelectStation({ label }) {
  return (
    <Card
      className="SelectStation"
      variant="subtle"
      color="purple"
      m="xxs"
      px="sm"
      py="xs"
      width="xxs"
    >
      <label>
        <Text>{label || 'Dep.'}</Text>
      </label>
      <Select>
        <option value="default" disabled={true}>
          역을 선택해주세요
        </option>
        <option>서울</option>
        <option>동대구</option>
        <option>부산</option>
      </Select>
    </Card>
  );
}

export default SelectStation;
