import { Card, Text } from 'dracula-ui';
import './LabelCard.css';

function LabelCard({ label, children }) {
  return (
    <Card
      className="LabelCard"
      variant="subtle"
      color="purple"
      m="xxs"
      px="sm"
      py="xs"
    >
      <label>
        <Text>{label || ''}</Text>
      </label>
      { children }
    </Card>
  );
}

export default LabelCard;
