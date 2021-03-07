<template>
  <div class="home">
    <div class="container">
      <div class="progress-container">
        <div class="progress" :style="progressStyle"></div>
        <div
          v-for="step in steps"
          :key="step"
          class="circle"
          :class="{ active: step <= current }"
        >
          {{ step }}
        </div>
      </div>

      <button class="btn" @click="prev" :disabled="prevDisabled">Prev</button>
      <button class="btn" @click="next" :disabled="nextDisabled">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class Home extends Vue {
  steps = 4;
  current = 1;

  get progressStyle() {
    return `width: ${((this.current - 1) / (this.steps - 1)) * 100}%`;
  }

  get prevDisabled() {
    return this.current === 1;
  }

  get nextDisabled() {
    return this.current === this.steps;
  }

  next() {
    this.current++;
    if (this.current > this.steps) {
      this.current = this.steps;
    }
  }
  prev() {
    this.current--;
    if (this.current < 1) {
      this.current = 1;
    }
  }
}
</script>

<style>

:root {
  --line-border-fill: hsl(135, 84%, 45%);
  --line-border-empty: hsla(135, 84%, 45%, 0.2);
}

body {
  background-color: hsla(135, 84%, 45%, 0.05);
  font-family: "Muli", sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  overflow: hidden;
  margin: 0;
}

.container {
  text-align: center;
}

.progress-container {
  display: flex;
  justify-content: space-between;
  position: relative;
  margin-bottom: 30px;
  max-width: 100%;
  width: 350px;
}

.progress-container::before {
  content: "";
  background-color: var(--line-border-empty);
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  height: 3px;
  width: 100%;
  z-index: -1;
}

.progress {
  background-color: var(--line-border-fill);
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  height: 3px;
  width: 0%;
  z-index: -1;
  transition: 0.3s ease;
}

.circle {
  background-color: #fff;
  color: #999;
  border-radius: 50%;
  height: 30px;
  width: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid var(--line-border-empty);
  transition: 0.3s ease 0.1s;
}

.circle.active {
  border-color: var(--line-border-fill);
}

.btn {
  background-color: var(--line-border-fill);
  color: #fff;
  border: 0;
  border-radius: 6px;
  cursor: pointer;
  font-family: inherit;
  padding: 8px 30px;
  margin: 5px;
  font-size: 16px;
  transition: 0.1s;
}

.btn:active {
  transform: translateY(1px);
}

.btn:focus {
  outline: 0;
}

.btn:disabled {
  background-color: var(--line-border-empty);
  cursor: not-allowed;
}
</style>