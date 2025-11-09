import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { SyncService } from '../../../core/services/sync.service';

@Component({
  selector: 'app-connection-indicator',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './connection-indicator.component.html',
  styleUrls: ['./connection-indicator.component.scss']
})
export class ConnectionIndicatorComponent implements OnInit, OnDestroy {
  isOnline = true;
  isSyncing = false;
  pendingCount = 0;
  showDetails = false;

  private subscriptions: Subscription[] = [];

  constructor(private syncService: SyncService) {}

  ngOnInit(): void {
    this.subscriptions.push(
      this.syncService.online$.subscribe(online => {
        this.isOnline = online;
      })
    );

    this.subscriptions.push(
      this.syncService.syncing$.subscribe(syncing => {
        this.isSyncing = syncing;
      })
    );

    this.subscriptions.push(
      this.syncService.pendingCount$.subscribe(count => {
        this.pendingCount = count;
      })
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  toggleDetails(): void {
    this.showDetails = !this.showDetails;
  }

  async forceSyncNow(): Promise<void> {
    if (this.isOnline && !this.isSyncing) {
      await this.syncService.syncPendingData();
    }
  }
}

