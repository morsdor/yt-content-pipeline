import { Composition } from 'remotion';
import './brand/fonts'; // module-level font loads — must be imported once, here
import { PlatePush } from './families/PlatePush';
import { TitleCard } from './scenes/TitleCard';

/**
 * Depth First — composition registry.
 *
 * Frame spec is fixed by brand_guide_software.md §5: 3840×2160 @ 30fps, and every scene
 * renders with 30 frames of handles at BOTH ends (Premiere conform stays trim-only).
 * A scene's durationInFrames = round(seconds × 30) + 60.
 *
 * `defaultProps` must stay an inline object literal — that is what lets Studio's Props
 * editor write visual edits back into this file.
 */

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="TitleCard"
        component={TitleCard}
        durationInFrames={150}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* Reference scene: 10s of content (300f) + 2×30f handles = 360f. */}
      <Composition
        id="Scene-PlatePush"
        component={PlatePush}
        durationInFrames={360}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'ai' as const,
          push: 4 as const,
          direction: 'in' as const,
          label: 'scene_01',
        }}
      />
    </>
  );
};
